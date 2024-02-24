from pydantic import BaseModel,Field
from datetime import datetime
class User(BaseModel): 
    firstName : str 
    lastName : str
    emailId :str
    dob :datetime.date
    address: str
    role : str
    
    


