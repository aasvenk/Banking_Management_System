from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from DB import models, database, schema
from utils import authBearer,utils
from datetime import datetime

router=APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404:{"description":"Not found"}}
)
SessionLocal=database.SessionLocal

def get_db():
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/getInternalUsersInfo')
async def getInternlUsersInfo(dependencies=Depends(authBearer.jwtBearer()),db:Session=Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()
    
    if utils.roleChecker("Admin",loggedIn.roles):
        # userInfo=db.query(models.UserInformation).filter(models.UserInformation.custId==userId).all()
        internalUserIds = db.query(models.Users).filter(models.Users.roles == 'Internal User').all()
        print(internalUserIds)
        if not internalUserIds:
            raise HTTPException(status_code=404, detail="No internal users found")
        userInfos=[]
        for user in internalUserIds:
            userInfos.append({
                "First Name":user.firstName,
                "Last Name":user.lastName,
                "email Id":user.emailId,
                "address":user.address
            })
        return userInfos

@router.get("/getLoginAttempts")
async def getLoginAttemptsInfo(dependencies=Depends(authBearer.jwtBearer()),db: Session = Depends(get_db)):
    tokenInst=db.query(models.TokenTable).filter(models.TokenTable.accessToken==dependencies).first()
    if not tokenInst:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId=tokenInst.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()
    
    loginAttemptsList = []
    if utils.roleChecker("Admin",loggedIn.roles):
        login_attempts = db.query(models.LoginAttempt).all()
        if login_attempts is None:
            raise HTTPException(status_code=404, detail="No login attempts found")
        
        for attempts in login_attempts:
            attempt_dict={
                "Email ID": attempts.emailId,
                "Attempt Status": attempts.loginStatus,
                "Message": attempts.message,
                "Roles":attempts.roles,
                "Time": attempts.timestamp.strftime("%m-%d-%Y %H:%M:%S"),
            }
            loginAttemptsList.append(attempt_dict)

    return loginAttemptsList

@router.get("/getAllUserInfo")
async def getAllUserInfo(dependencies = Depends(authBearer.jwtBearer()),db : Session = Depends(get_db)):
    token=token = db.query(models.TokenTable).filter(models.TokenTable.accessToken == dependencies).first()
    if not token:
        raise HTTPException(status_code=404, detail="User not logged In")
    userId = token.userId
    user=db.query(models.Users).filter(models.Users.id==userId).first()
    if not user:
        raise HTTPException(status_code=404, detail="UserInfo not found")
    if utils.roleChecker("Admin",user.roles):
        userInfos=db.query(models.UserInformation).all()
        print(userInfos)
        result = [u.__dict__ for u in userInfos]
        for r in result:
            r.pop('_sa_instance_state', None)
        return result
    

@router.delete("/deleteUser/{emailId}", status_code=200)
def delete_user(emailId: str, db: Session = Depends(get_db), dependencies= Depends(authBearer.jwtBearer())):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token :
        raise HTTPException (status_code= 404, detail= 'User not logged in')

    userId=token.userId
    loggedIn = db.query(models.Users).filter(models.Users.id == userId).first()

    if utils.roleChecker("Admin",loggedIn.roles):
        user = db.query(models.Users).filter(models.Users.emailId == emailId).first()
    
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        userInformationSavingQuery= db.query(models.UserInformation).filter(models.UserInformation.emailId == user.emailId,models.UserInformation.accountType=='Saving').first()
        userInformationCheckingQuery = db.query(models.UserInformation).filter(models.UserInformation.emailId == user.emailId,models.UserInformation.accountType=='Checking').first()

        try : 
            selfTransferQuery = db.query(models.SelfBankStatements).filter(models.SelfBankStatements.emailId == user.emailId).all()
            if not selfTransferQuery:
                pass
            else:
                selfTransferResult = db.query(models.SelfBankStatements).filter(models.SelfBankStatements.emailId == user.emailId).delete()
                db.commit()
            accountTransferQuery = db.query(models.AccountBankStatement).filter((models.AccountBankStatement.fromEmail ==emailId) | (models.AccountBankStatement.toEmail == emailId)).all()
            if not accountTransferQuery:
                pass

            else: 
                accountTransferResult = db.query(models.AccountBankStatement).filter((models.AccountBankStatement.fromEmail ==emailId) | (models.AccountBankStatement.toEmail == emailId)).delete()
                db.commit()
            if not userInformationSavingQuery and not userInformationCheckingQuery:
                pass
            else: 
                if userInformationSavingQuery:
                    transferRequestSavingQuery = db.query(models.TransferRequest).filter((models.TransferRequest.fromAccountNumber == userInformationSavingQuery.accountNumber)|(models.TransferRequest.toAccountNumber == userInformationSavingQuery.accountNumber)).all()
                    if not transferRequestSavingQuery:
                        pass
                    else:
                        transferRequestResult = db.query(models.TransferRequest).filter((models.TransferRequest.fromAccountNumber == userInformationSavingQuery.accountNumber)|(models.TransferRequest.toAccountNumber == userInformationSavingQuery.accountNumber)).delete()
                        db.commit()
                if userInformationCheckingQuery:
                    transferRequestCheckingQuery = db.query(models.TransferRequest).filter((models.TransferRequest.fromAccountNumber == userInformationCheckingQuery.accountNumber)|(models.TransferRequest.toAccountNumber == userInformationSavingQuery.accountNumber)).all()
                    if not transferRequestCheckingQuery:
                        pass
                    else:
                        transferRequestResult = db.query(models.TransferRequest).filter((models.TransferRequest.fromAccountNumber == userInformationCheckingQuery.accountNumber)|(models.TransferRequest.toAccountNumber == userInformationSavingQuery.accountNumber)).delete()
                        db.commit()
                if not userInformationSavingQuery:
                    pass
                else:
                    userInformationSavingResult = db.query(models.UserInformation).filter(models.UserInformation.emailId == user.emailId,models.UserInformation.accountType=='Saving').delete()
                    db.commit()
                if not userInformationCheckingQuery:
                    pass
                else: 
                    userInformationSavingResult = db.query(models.UserInformation).filter(models.UserInformation.emailId == user.emailId,models.UserInformation.accountType=='Checking').delete()
                    db.commit()
            tokenQuery = db.query(models.TokenTable).filter(models.TokenTable.userId == user.id).all()
            
            if not tokenQuery: 
                pass
            else:
                tokenResult= db.query(models.TokenTable).filter(models.TokenTable.userId == user.id).delete()
                db.commit()
                UserResult = db.query(models.Users).filter(models.Users.emailId == user.emailId).delete()
                db.commit()
            return {"message": "User deleted successfully"}

        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))