from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from DB import schema, models, database
import random
from utils import authBearer, utils

router=APIRouter(
    prefix="/userInfo",
    tags=["userInfo"],
    responses={404:{"description":"Not found"}}
)
SessionLocal=database.SessionLocal

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@router.post("/createUserInfo")
async def createUserInfo(userInfo:schema.userInfo,db:Session=Depends(get_db)):
    userInfoModel=models.UserInformation()
    userInfoModel.emailId=userInfo.emailId
    userInfoModel.accountType=userInfo.accountType
    userInfoModel.accountBalance=userInfo.accountBalance
    userInfoModel.phoneNo = userInfo.phoneNo

    # if utils.roleChecker(["Internal User"],user.roles):
    user=db.query(models.Users).filter(models.Users.emailId==userInfo.emailId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    userInfoModel.custId=user.id
    userInfoModel.address = user.address
    userInfoModel.accountNumber=random.randint(1000000000,9999999999)
    db.add(userInfoModel)
    db.commit()

@router.get("/getUserInfo")
async def getUserInfo(dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    userInfo=db.query(models.UserInformation).filter(models.UserInformation.custId==userId).all()
    if not userInfo:
        raise HTTPException(status_code=404, detail="UserInfo not found")
    
    userInfoList = []

    for user in userInfo:
        user_dict = {
            "emailId": user.emailId,
            "accountNumber": user.accountNumber,
            "phoneNumber": user.phoneNo,
            "address": user.address,
            "routingNumber": user.routingNumber,
            "accountType": user.accountType,
            "accountBalance": user.accountBalance
        }
        userInfoList.append(user_dict)
    return userInfoList

@router.patch("/updateUser")
async def updateUser(userInfoUpdateData:schema.userInfoUpdate,dependencies = Depends(authBearer.jwtBearer()),db : Session = Depends(get_db)):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken == dependencies).first()
    if not token:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId = token.userId
    userInfo = db.query(models.UserInformation).filter(models.UserInformation.custId == userId).all()
    if not userInfo:
        raise HTTPException(status_code=404, detail="UserInfo not found")
    
    userInfoUpdate= userInfoUpdateData.model_dump(exclude_unset= True)

    UserUpdate = db.query(models.Users).filter(models.Users.id == userId).first()

    if "address" in userInfoUpdate:
        UserUpdate.address = userInfoUpdate["address"]

    for user in userInfo:
        for key, value in userInfoUpdate.items():
            setattr(user, key, value)
    db.commit()
    return {"message":"Successfully Updated data"}

@router.get("/getAllUserInfo")
async def getAllUserInfo(dependencies = Depends(authBearer.jwtBearer()),db : Session = Depends(get_db)):
    token=token = db.query(models.TokenTable).filter(models.TokenTable.accessToken == dependencies).first()
    if not token:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId = token.userId
    user=db.query(models.Users).filter(models.Users.id==userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="UserInfo not found")
    if utils.roleChecker(["Admin"],user.roles):
        userInfos=db.query(models.UserInformation).all()
        print(userInfos)
        result = [u.__dict__ for u in userInfos]
        for r in result:
            r.pop('_sa_instance_state', None)
        return result