from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from enum import Enum
from DB.database import Base
from sqlalchemy.types import Date


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index= True)
    firstName = Column(String,nullable=False)
    lastName = Column(String,nullable=False)
    emailId = Column(String, unique=True,nullable=False)
    password=Column(String, nullable=False)
    dob= Column(Date,nullable=False)
    address = Column(String,nullable=False)
    role = Column(String,default="Customer")
    # userInfo= relationship("UserInformation", back_populates="userRegister")


# class UserInformation(Base):
#     __tablename__ = "UserInformation"

#     id = Column(Integer, primary_key=True,index= True)
#     emailId =Column(String, ForeignKey('Users.emailId'),unique= True)
#     accountNumber = Column(Integer)
#     custId =Column(String)
#     accountType =Column(String)
#     accountBalance =Column(Float)
#     userRegister=relationship("Users", back_populates="userInfo")
    
