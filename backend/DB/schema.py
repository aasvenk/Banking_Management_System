from pydantic import BaseModel,Field
from datetime import datetime, date
class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    dob :date
    address: str
    role : str
    
    


