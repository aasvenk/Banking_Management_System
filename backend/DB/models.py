from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from DB.database import Base
from datetime import datetime,time

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True,index= True)
    firstName = Column(String)
    lastName = Column(String)
    emailId = Column(String)
    dob= Column(datetime.date)
    address = Column(String)
    role = Column(String)