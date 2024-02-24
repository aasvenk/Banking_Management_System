from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date

from DB.database import Base
from datetime import datetime,time

class UserRegistration(Base):
    __tablename__ = "UserRegistration"

    id = Column(Integer, primary_key=True,index= True)
    firstName = Column(String)
    lastName = Column(String)
    emailId = Column(String)
    dob= Column(Date)
    address = Column(String)
    role = Column(String)
    userInfo= relationship("UserInformation", back_populates="userRegister")

class UserInformation(Base):
    __tablename__ = "UserInformation"

    id = Column(Integer, primary_key=True,index= True)
    emailId =Column(String, ForeignKey('UserRegistration.emailId'))
    accountNumber = Column(Integer)
    custId =Column(String)
    accountType =Column(String)
    accountBalance =Column(Float)
    userRegister=relationship("UserRegistration", back_populates="userInfo")