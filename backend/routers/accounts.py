from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
import random
from DB import models, database, schema
from utils import authBearer,utils

router=APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404:{"description":"Not found"}}
)
SessionLocal=database.SessionLocal

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

# Display account details of a particular user using their emailId
@router.post("/createUserInfo")
async def createUserInfo(userInfo:schema.userInfo,dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

    if utils.roleChecker("Internal User",loggedIn.roles):
        userInfoModel=models.UserInformation()
        userInfoModel.emailId=userInfo.emailId
        userInfoModel.accountType=userInfo.accountType
        userInfoModel.accountBalance=userInfo.accountBalance
        userInfoModel.phoneNo = userInfo.phoneNo
        user=db.query(models.Users).filter(models.Users.emailId==userInfo.emailId).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        userisInternal=db.query(models.Users).filter(models.Users.emailId==userInfo.emailId,models.Users.roles=="Internal User").first()
        if  userisInternal:
            raise HTTPException(status_code=404, detail="Invalid user role type")
        userIsAdmin=db.query(models.Users).filter(models.Users.emailId==userInfo.emailId,models.Users.roles=="Admin").first()
        if  userIsAdmin:
            raise HTTPException(status_code=404, detail="Invalid user role type")
        userInfoModel.custId=user.id
        userInfoModel.address = user.address
        userInfoModel.accountNumber=random.randint(1000000000,9999999999)
        db.add(userInfoModel)
        db.commit()
        return {"message":"User Info created successfully"}
    
@router .post('/getUserAccDetails')
async def getUserAccDetails(emailDetail:schema.emailDetail,dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

    if utils.roleChecker("Internal User",loggedIn.roles):
        user=db.query(models.Users).filter(models.Users.emailId==emailDetail.emailId, models.Users.roles=="Customer").first()
        if not user:
            raise HTTPException(status_code=404, detail="Customer not found")

        userInfo=db.query(models.UserInformation).filter(models.UserInformation.emailId==user.emailId).all()
        if not userInfo:
            raise HTTPException(status_code=404, detail="User account details not found")
        print(userInfo)
        userAccList=[]
        for user in userInfo:
            user_dict={
                "emailId": user.emailId,
                "accountNumber": user.accountNumber,
                "accountType": user.accountType,
                "accountBalance": user.accountBalance
            }
            userAccList.append(user_dict)

    return userAccList

# Edit account balance of a user for a particular account type
@router.patch("/updateUserAccDetails")
async def updateUser(emailDetail: schema.emailDetail, userAccUpdate: schema.userAccUpdate, dependencies=Depends(authBearer.jwtBearer()), db: Session=Depends(get_db)): 
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()
    user = db.query(models.Users).filter(models.Users.emailId == emailDetail.emailId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if utils.roleChecker("Internal User",loggedIn.roles):
        query = db.query(models.UserInformation).filter(models.UserInformation.emailId == user.emailId)
        if userAccUpdate.accountType is not None:
            query = query.filter(models.UserInformation.accountType == userAccUpdate.accountType)
        
        userInfo = query.all()
        if not userInfo:
            raise HTTPException(status_code=404, detail="User account information not found for the specified account type")
        
        userInfoUpdate = userAccUpdate.dict(exclude_unset=True)
        
        userUpdate = db.query(models.Users).filter(models.Users.emailId == user.emailId).first()
        
        if "address" in userInfoUpdate:
            userUpdate.address = userInfoUpdate["address"]
            del userInfoUpdate["address"]
            
        if "phoneNo" in userInfoUpdate:
            userUpdate.phoneNo = userInfoUpdate["phoneNo"]
            del userInfoUpdate["phoneNo"]

        for user_info in userInfo:
            for key, value in userInfoUpdate.items():
                setattr(user_info, key, value)
        
        db.commit()
    return "User Account Updated Successfully"

# Delete an account of a user
@router.delete('/deleteUserAccDetails')
async def deleteUserAccDetails(deleteDetails: schema.deleteDetails, dependencies=Depends(authBearer.jwtBearer()), db: Session=Depends(get_db)): 
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

    if utils.roleChecker("Internal User",loggedIn.roles):
        user_info = db.query(models.UserInformation).filter(models.UserInformation.emailId == deleteDetails.emailId, models.UserInformation.accountNumber == deleteDetails.accountNo).first()
        if not user_info:
            raise HTTPException(status_code=404, detail="User account details not found")
        
        db.delete(user_info)
        db.commit()

    return "User account details successfully deleted"

