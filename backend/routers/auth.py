from fastapi import APIRouter,Depends, HTTPException, status
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
import utils
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



    
