from pydantic import BaseModel,UUID4
from datetime import date
from typing import Optional
from enum import Enum



class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    password:str
    dob :date
    address: str
    roles:str

    
class requestDetails(BaseModel):
    emailId:str
    password:str
    totpToken:str

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

class emailDetail(BaseModel):
    emailId:str
    
class accountTransfer(BaseModel):
    fromAccountType: str
    toAccountNumber:int
    toRoutingNumber: int
    transferBalance: float
    totpToken:str

class userAccUpdate(BaseModel):
    accountType: Optional[str] = None
    accountBalance : Optional[str] = None

class deleteDetails(BaseModel):
    emailId: str
    accountNo: int
class getCustAccInfo(BaseModel):
    emailId: str
    accountType: str



