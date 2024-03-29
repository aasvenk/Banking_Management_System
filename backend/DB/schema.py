from pydantic import BaseModel,UUID4
from datetime import date
from typing import Optional
from uuid import UUID

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

class selfTransferMoney(BaseModel):
    fromAccountType:str
    toAccountType:str
    transferAmount:float

# class UserInformation(BaseModel):
#     emailId :str
#     accountNumber: int
#     custId: str
#     accountType: str
#     accountBalance: float
    
class accountTransfer(BaseModel):
    fromAccountType: str
    toAccountNumber:int
    toRoutingNumber: int
    transferBalance: float



