from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from DB.database import Base
from sqlalchemy.types import Date
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True,index= True)
    firstName = Column(String)
    lastName = Column(String)
    emailId = Column(String)
    dob= Column(Date)
    address = Column(String)
    role = Column(String)