from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from DB import schema, models, database
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


@router.post("/getUserInfo")
async def getUserInfo(emailId:schema.emailDetail,dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

    if utils.roleChecker("Customer",loggedIn.roles):
        user=db.query(models.Users).filter(models.Users.emailId==emailId.emailId).first()
        userInfo=db.query(models.UserInformation).filter(models.UserInformation.emailId==user.emailId).all()
        if not userInfo:
            raise HTTPException(status_code=404, detail="User account details not found")
        userInfoList = []
        print(userInfo)
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


# @router.post("/getUserInfo")
# async def getUserInfo(emailId:schema.emailDetail,dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
#     tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
#     if not tokenInst:
#         raise HTTPException(status_code=404, detail="User not logged In")
#     userId=tokenInst.userId
#     loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

#     if utils.roleChecker(["Internal User"],loggedIn.roles):
#         user=db.query(models.Users).filter(models.Users.emailId==emailId.emailId).first()
#         userInfo=db.query(models.UserInformation).filter(models.UserInformation.emailId==user.emailId).all()
#         if not userInfo:
#             raise HTTPException(status_code=404, detail="User account details not found")
#         userInfoList = []
#         print(userInfo)
#         for user in userInfo:
#             user_dict = {
#                 "emailId": user.emailId,
#                 "accountNumber": user.accountNumber,
#                 "phoneNumber": user.phoneNo,
#                 "address": user.address,
#                 "routingNumber": user.routingNumber,
#                 "accountType": user.accountType,
#                 "accountBalance": user.accountBalance
#             }
#             userInfoList.append(user_dict)
#     return userInfoList

@router.patch("/updateUser")
async def updateUser(userInfoUpdateData:schema.userInfoUpdate,dependencies = Depends(authBearer.jwtBearer()),db : Session = Depends(get_db)):
    
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    
    loggedInuserId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == loggedInuserId).first()

    if utils.roleChecker("Customer",loggedIn.roles):

        userInfo = db.query(models.UserInformation).filter(models.UserInformation.emailId == loggedIn.emailId).all()
        if not userInfo:
            raise HTTPException(status_code=404, detail="UserInfo not found")
        
        userInfoUpdate= userInfoUpdateData.model_dump(exclude_unset= True)

        UserUpdate = db.query(models.Users).filter(models.Users.emailId == loggedIn.emailId).first()

        if "address" in userInfoUpdate:
            UserUpdate.address = userInfoUpdate["address"]

        for user in userInfo:
            for key, value in userInfoUpdate.items():
                setattr(user, key, value)
    db.commit()
    return {"message":"Successfully Updated data"}


    
