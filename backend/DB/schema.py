from pydantic import BaseModel,Field
from datetime import date
class UserRegistration(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    dob :date
    address: str
    role : str

class UserInformation(BaseModel):
    emailId :str
    accountNumber: int
    custId: str
    accountType: str
    accountBalance: float
    


    
    


