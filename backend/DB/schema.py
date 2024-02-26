from pydantic import BaseModel,UUID4
from datetime import date

class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    password:str
    dob :date
    address: str
    role : str

class requestDetails(BaseModel):
    emailId:str
    password:str

class tokenSchema(BaseModel):
    accessToken:str
    refreshToken:str


# class UserInformation(BaseModel):
#     emailId :str
#     accountNumber: int
#     custId: str
#     accountType: str
#     accountBalance: float
    


    
    


