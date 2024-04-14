from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
from utils import utils
from utils import authBearer
from fastapi.responses import JSONResponse
import os
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
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT EMAIL ID!!")

    hashedPassword=user.password
    if not utils.verifyPassword(requestDetails.password,hashedPassword):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT PASSWORD!!")
    
    totp = TOTP(user.totpSecret)
    if not totp.verify(requestDetails.totpToken):
        raise HTTPException(status_code=400,detail= "Invalid 2FA token")
    
    access=utils.createAccessToken(user.id)
    refresh=utils.createRefreshToken(user.id)

    token=models.TokenTable(userId=user.id, accessToken=access, refreshToken=refresh, status=True)
    db.add(token)
    db.commit()
    db.refresh(token)
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
    #Check later if required
    # info=[]
    # for record in tokenRecord:
    #     if (datetime.utcnow - record.createdDate).total_seconds()/60 > 60:
    #         info.append(record.userId)

    # existingToken= db.query(models.TokenTable).filter(models.TokenTable.userId == userId, models.TokenTable.accessToken == token).first()
    # if existingToken:
    #     existingToken.status=False
    #     db.delete(existingToken)
    #     db.commit()
    #     db.refresh()
    # return {"message":"Logout Successful"}
    
    
    existingToken = db.query(models.TokenTable).filter(models.TokenTable.userId== userId).all()
    if existingToken: 
        for token in existingToken :
            token.status = False
            db.delete(token)
            db.commit()
    return {"message":"Logout Successful"}
    
