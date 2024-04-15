from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
from utils import utils
from utils import authBearer
from fastapi.responses import StreamingResponse
import os
import qrcode
from io import BytesIO
from dotenv import load_dotenv
from pyotp import random_base32,TOTP



SessionLocal=database.SessionLocal

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

def get_db(): 
    try :
        db= SessionLocal()
        yield db
    finally:
        db.close()

# load_dotenv() 
# GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID') or None
# GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET') or None
# if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
#     raise BaseException('Missing env variables')





@router .post("/register",status_code=200)
async def registeration(user:schema.User,db:Session=Depends(get_db)):
    userModel=models.Users()
    # if user.emailId  == db.query(models.Users).filter(models.Users.emailId== user.emailId).first().emailId is not None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ID already Exists ")
    if not (user.roles =="Customer" or user.roles =="Internal User" or user.roles=="Admin"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Allowed user role type: Customer or Internal User or admin")
    
    existAdmin=db.query(models.Users).filter(models.Users.roles=="Admin").first()
    if existAdmin and user.roles=="Admin":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admin already exists")
    userModel.address=user.address
    userModel.lastName=user.lastName
    userModel.firstName=user.firstName
    userModel.dob=user.dob
    userModel.emailId=user.emailId
    userModel.password=str(utils.getHashPassword(user.password))
    userModel.roles=user.roles
    userModel.totpSecret = random_base32() 
    db.add(userModel)
    db.commit()
    totpUri = TOTP(userModel.totpSecret).provisioning_uri(userModel.emailId,issuer_name="banking_system")
    return {"Message":"User registered Successfully","totpUri":totpUri}




@router .post("/login")
async def login(requestDetails:schema.requestDetails, db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.emailId==requestDetails.emailId).first()
    login_attempt = models.LoginAttempt(emailId=requestDetails.emailId)
    if user is None:
        login_attempt.message = "Incorrect Email ID"
        db.add(login_attempt)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT EMAIL ID!!")

    hashedPassword=user.password
    if not utils.verifyPassword(requestDetails.password,hashedPassword):
        login_attempt.message = "Incorrect Password"
        db.add(login_attempt)
        db.commit()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT PASSWORD!!")
    
    totp = TOTP(user.totpSecret)
    if not totp.verify(requestDetails.totpToken):
        login_attempt.message = "Invalid 2FA token"
        db.add(login_attempt)
        db.commit()
        raise HTTPException(status_code=400,detail= "Invalid 2FA token")
    
    access=utils.createAccessToken(user.id)
    refresh=utils.createRefreshToken(user.id)

    token=models.TokenTable(userId=user.id, accessToken=access, refreshToken=refresh, status=True)
    db.add(token)
    db.commit()
    db.refresh(token)
    login_attempt.loginStatus = True
    login_attempt.message = "Login successful"
    login_attempt.roles=user.roles
    db.add(login_attempt)
    db.commit()
    return{
        "accessToken":access,
        "refreshToken":refresh
    }

@router .post('/logout')
async def logout(dependencies=Depends(authBearer.jwtBearer()),db: Session=Depends(get_db)):
    token = dependencies
    payload= authBearer.decodeJwt(token)
    userId=payload['sub']
    tokenRecord=db.query(models.TokenTable).all()
     
    existingToken = db.query(models.TokenTable).filter(models.TokenTable.userId== userId).all()
    if existingToken: 
        for token in existingToken :
            token.status = False
            db.delete(token)
            db.commit()
    return {"message":"Logout Successful"}

@router.get("/qr")
def generate_qr(totpURL: str):
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(totpURL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    img_bytes = BytesIO()
    img.save(img_bytes)
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/jpeg", headers={
        "Content-Disposition": f"attachment; filename=qr_code.jpg"
    })
    
