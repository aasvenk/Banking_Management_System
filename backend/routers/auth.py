from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
from utils import utils
from utils import authBearer
from jose import jwt
from datetime import datetime, timedelta
from jwt.exceptions import InvalidTokenError

engine=database.engine
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

@router .post("/register")
async def registeration(user:schema.User,db:Session=Depends(get_db)):
    user_model=models.Users()
    user_model.address=user.address
    user_model.lastName=user.lastName
    user_model.firstName=user.firstName
    user_model.dob=user.dob
    user_model.emailId=user.emailId
    user_model.password=str(utils.getHashPassword(user.password))
    user_model.role=user.role
    db.add(user_model)
    db.commit()


@router .post("/login")
async def login(requestDetails:schema.requestDetails, db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.emailId==requestDetails.emailId).first()
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT EMAIL ID!!")

    hashedPassword=user.password
    if not utils.verifyPassword(requestDetails.password,hashedPassword):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INCORRECT PASSWORD!!")
    
    access=utils.createAccessToken(user.id)
    refresh=utils.createRefreshToken(user.id)

    token=models.TokenTable(userId=str(user.id), accessToken=access, refreshToken=refresh, status=True)
    db.add(token)
    db.commit()
    db.refresh(token)
    return{
        "accessToken":access,
        "refreshToken":refresh
    }

@router .post('/logout')
def logout(dependencies=Depends(authBearer.jwtBearer()),db: Session=Depends(get_db)):
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
        for Token in existingToken :
            Token.status = False
            db.commit()
    return {"message":"Logout Successful"}
    
