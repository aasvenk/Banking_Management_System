from pydantic import BaseModel,Field
from datetime import datetime, date
from datetime import date

class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    password:str
    dob :date
    address: str
    role : str

# class UserInformation(BaseModel):
#     emailId :str
#     accountNumber: int
#     custId: str
#     accountType: str
#     accountBalance: float
    


    
    


