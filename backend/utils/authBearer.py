from jose import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from DB.models import TokenTable
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_KEY=os.getenv('JWT_REFRESH_KEY')
ALGORITHM=os.getenv('ALGORITHM')

def decodeJwt(jwtToken: str):
    try:
        payload = jwt.decode(jwtToken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except InvalidTokenError:
        return None
    
class jwtBearer(HTTPBearer):
    def __init__(self,auto_error: bool=True):
        super(jwtBearer,self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials:HTTPAuthorizationCredentials=await super(jwtBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")
            if not self.verifyJwt(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            
            return credentials.credentials
        
        else:
            raise HTTPException(status_code=403, detail="Invalid authorrization code")
        
        
    def verifyJwt(self,jwtToken):
        try:
            payload= decodeJwt(jwtToken)
        except:
            payload = None
        if payload:
            return True
        return False
    
jwtBearerObj = jwtBearer() 



    

