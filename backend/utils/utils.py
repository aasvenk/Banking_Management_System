from fastapi import Depends,HTTPException
from sqlalchemy.orm import Session
from DB import schema, models, database
from passlib.context import CryptContext
from typing import Union, Any
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from jose import jwt
from typing import List
from .authBearer import decodeJwt,jwtBearer



load_dotenv()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_KEY=os.getenv('JWT_REFRESH_KEY')
ACCESS_TOKEN_EXPIRE_TIME=int(os.getenv('ACCESS_TOKEN_EXPIRE_TIME'))
REFRESH_TOKEN_EXPIRE_TIME=int(os.getenv('REFRESH_TOKEN_EXPIRE_TIME'))
ALGORITHM=os.getenv('ALGORITHM')
#defining a context that handles hashing
passwordContext= CryptContext(schemes=["bcrypt"],deprecated="auto")

SessionLocal=database.SessionLocal
def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

#Using the context to hash the password and return the hashed pwd.
def getHashPassword(password):
    return passwordContext.hash(password)

def verifyPassword(passowrd,hashedPassword):
    return passwordContext.verify(passowrd,hashedPassword)

def createAccessToken(subject:Union[str,Any]):
    expires_delta=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    toEncode = {"exp" : expires_delta, "sub":str(subject)}
    encodedJwt= jwt.encode(toEncode,JWT_SECRET_KEY,ALGORITHM)
    return encodedJwt

def createRefreshToken(subject:Union[str,Any]):
    expires_delta=datetime.utcnow()+timedelta(minutes=REFRESH_TOKEN_EXPIRE_TIME)
    toEncode = {"exp" : expires_delta, "sub":str(subject)}
    encodedJwt= jwt.encode(toEncode,JWT_REFRESH_KEY,ALGORITHM)
    return encodedJwt

def roleChecker(requiredRoles:List, userRoles):
    if not any(role in userRoles for role in requiredRoles):
        raise HTTPException(
                status_code=403, detail="Operation not permitted"
            )
    return True
    