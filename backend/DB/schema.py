from pydantic import BaseModel,UUID4
from datetime import date
from typing import Optional,List
from enum import Enum



class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    password:str
    dob :date
    address: str
    roles:List[str]

    
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
    
class emailDetail(BaseModel):
    emailId:str
    
class userAccUpdate(BaseModel):
    accountType: Optional[str] = None
    accountBalance : Optional[str] = None
    
    


