from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from enum import Enum
from DB.database import Base
import datetime
from sqlalchemy.sql import func
import uuid

class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,index=True)
    firstName = Column(String,nullable=False)
    lastName = Column(String,nullable=False)
    emailId = Column(String, unique=True,nullable=False)
    password=Column(String, nullable=False)
    dob= Column(Date,nullable=False)
    address = Column(String,nullable=False)
    roles = Column(String,nullable=False)
    totpSecret = Column(String, nullable= True)
    userCustId= relationship("UserInformation", back_populates="userId", foreign_keys="UserInformation.custId")
    userEmailId=relationship("UserInformation",back_populates="userEmail",foreign_keys="UserInformation.emailId")
    accEmailId = relationship("SelfBankStatements", back_populates="accountEmailId", foreign_keys="SelfBankStatements.emailId")
    fromAccEmail= relationship("AccountBankStatement", back_populates="fromEmailPop", foreign_keys="AccountBankStatement.fromEmail")
    toAccEmail= relationship("AccountBankStatement", back_populates="toEmailPop", foreign_keys="AccountBankStatement.toEmail")

class TokenTable(Base):
    __tablename__="token"
    userId=Column(UUID(as_uuid=True))
    accessToken=Column(String,primary_key=True)
    refreshToken=Column(String, nullable=False)
    status=Column(Boolean)
    createdDate=Column(DateTime,default=datetime.datetime.now)
    
class UserInformation(Base):
    __tablename__ = "userinformation"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,index=True)
    emailId =Column(String, ForeignKey('users.emailId'), nullable=False)
    phoneNo=Column(String,nullable=False)
    address=Column(String,nullable=False)
    accountNumber = Column(BigInteger,nullable=False, unique=True)
    routingNumber=Column(Integer,nullable=False,default=2081678945)
    custId =Column(UUID(as_uuid=True),ForeignKey('users.id'),nullable=False)
    accountType =Column(String,nullable=False)
    accountBalance =Column(Float,nullable=False)
    userId=relationship("Users", back_populates="userCustId",foreign_keys=[custId])
    userEmail=relationship("Users",back_populates="userEmailId",foreign_keys=[emailId])
    userAccountNo = relationship("TransferRequest",back_populates= "userAccountNumber", foreign_keys= "TransferRequest.fromAccountNumber")
    fromAcc = relationship("AccountBankStatement",back_populates= "fromAccNumber", foreign_keys= "AccountBankStatement.fromAccountNumber")
    toAcc = relationship("AccountBankStatement",back_populates="toAccNumber",foreign_keys="AccountBankStatement.toAccountNumber")

class TransferRequest(Base):
    __tablename__ = "transferrequests"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,index=True)
    fromAccountNumber = Column(BigInteger, ForeignKey('userinformation.accountNumber'))
    toAccountNumber = Column(BigInteger, index=True)
    toRoutingNumber = Column(Integer, index=True)
    amount = Column(Float)
    approved = Column(Boolean, default=False)
    userAccountNumber = relationship("UserInformation", back_populates= "userAccountNo", foreign_keys= [fromAccountNumber])


class SelfBankStatements(Base):
    __tablename__ = "selfbankstatements"  
    id  = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,index=True)
    emailId =Column(String, ForeignKey('users.emailId'), nullable=False)
    accountType = Column(String, index=True) 
    transactionType = Column(String, index=True)  
    amount = Column(Float) 
    balance = Column(Float,nullable= False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now()) 
    accountEmailId = relationship("Users", back_populates="accEmailId", foreign_keys=[emailId])

class AccountBankStatement(Base):
     __tablename__ = "accountbankstatement"
     id = Column (UUID(as_uuid=True), primary_key=True,default=uuid.uuid4,index=True) 
     transferId = Column(UUID(as_uuid=True),ForeignKey('transferrequests.id'), nullable=False)
     fromAccountNumber = Column(BigInteger, ForeignKey('userinformation.accountNumber'))
     toAccountNumber=Column(BigInteger,ForeignKey('userinformation.accountNumber'))
     fromEmail=Column(String,ForeignKey('users.emailId'),nullable=False)
     toEmail=Column(String,ForeignKey('users.emailId'),nullable=False)
     amount = Column(Float)
     balance = Column(Float,nullable=False)
     transactionType = Column(String)
     timestamp=Column(DateTime(timezone=True), server_default=func.now())
     fromAccNumber = relationship("UserInformation", back_populates= "fromAcc", foreign_keys= [fromAccountNumber])
     statmentEmailId=Column(String,nullable=False)
     toAccNumber=relationship("UserInformation", back_populates= "toAcc", foreign_keys= [toAccountNumber])
     fromEmailPop=relationship("Users", back_populates="fromAccEmail", foreign_keys=[fromEmail])
     toEmailPop=relationship("Users", back_populates="toAccEmail", foreign_keys=[toEmail])


class LoginAttempt(Base):
    __tablename__ = "loginattempts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    emailId = Column(String, nullable=False)
    loginStatus = Column(Boolean, default=False) 
    message = Column(String, nullable=False)
    roles = Column(String, default=['None'])
    timestamp = Column(DateTime, default=datetime.datetime.now)