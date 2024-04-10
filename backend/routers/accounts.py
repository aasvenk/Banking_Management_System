from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from DB import models, database, schema
from utils import authBearer

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

@router .post('/getUserAccDetails')
async def getUserAccDetails(emailDetail:schema.emailDetail,dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    # tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    user=db.query(models.Users).filter(models.Users.emailId==emailDetail.emailId).first()
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


@router.patch("/updateUserAccDetails")
async def updateUser(emailDetail: schema.emailDetail, userAccUpdate: schema.userAccUpdate, dependencies=Depends(authBearer.jwtBearer()), db: Session=Depends(get_db)): 
    user = db.query(models.Users).filter(models.Users.emailId == emailDetail.emailId).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
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
    return "User Updated Successfully"