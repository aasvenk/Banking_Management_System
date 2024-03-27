from pydantic import BaseModel,UUID4
from datetime import date
from typing import Optional

class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    password:str
    dob :date
    address: str

    
class requestDetails(BaseModel):
    emailId:str
    password:str

class tokenSchema(BaseModel):
    accessToken:str
    refreshToken:str

class userInfo(BaseModel):
    emailId:str
    accountType:str
    accountBalance:float
    phoneNo:str

class userInfoUpdate(BaseModel):
    phoneNo: Optional[str] = None
    address : Optional[str] = None

# class UserInformation(BaseModel):
#     emailId :str
#     accountNumber: int
#     custId: str
#     accountType: str
#     accountBalance: float
    


    
    


