from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
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
    user_model.role=user.role
    db.add(user_model)
    db.commit()
