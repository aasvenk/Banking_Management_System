from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
from utils import authBearer


SessionLocal=database.SessionLocal

router=APIRouter(
    prefix="/transfer",
    tags=["transactions"],
    responses={404: {"description": "Not found"}}
)

def get_db(): 
    try :
        db= SessionLocal()
        yield db
    finally:
        db.close()

@router.post("/selfTransfer",status_code=200)
def selfTransfer(transferDetails: schema.selfTransferMoney,dependencies = Depends(authBearer.jwtBearer()),db:Session = Depends(get_db)):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token:
        raise HTTPException(status_code= 404, detail = 'User not Logged In')
    
    userId = token.userId
    
    if transferDetails.fromAccountType != "Saving" or transferDetails.toAccountType != "Checking":
        if transferDetails.fromAccountType != "Checking" or transferDetails.toAccountType != "Saving":
                raise HTTPException(status_code=400, detail="Unsupported account type for transfer.")
    
    userInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId).all()
    if len(userInfo) ==0 :
        raise HTTPException(status_code= 401, detail = 'Account needs to be updated by Bank Employee with User Information')
    elif len(userInfo) == 1: 
        accountType = userInfo[0].accountType
        raise HTTPException(status_code= 400,detail = "You have only "+ accountType+" account. You need to have more than one account to self transfer funds")
    else:
        if transferDetails.fromAccountType== "Saving" and transferDetails.toAccountType =="Checking":
            senderUserInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId,models.UserInformation.accountType =='Saving').first()
            receiverUserInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId,models.UserInformation.accountType == 'Checking').first()
            if senderUserInfo.accountBalance < transferDetails.transferAmount:
                  raise HTTPException(status_code= 403, detail = 'Insufficient funds')
            else:
                senderUserInfo.accountBalance -= transferDetails.transferAmount
                receiverUserInfo.accountBalance += transferDetails.transferAmount
                db.commit()
                return "Transfer funds completed successfully"
        
        if transferDetails.fromAccountType== "Checking" and transferDetails.toAccountType =="Saving":
            senderUserInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId,models.UserInformation.accountType =='Checking').first()
            receiverUserInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId,models.UserInformation.accountType == 'Saving').first()
            if senderUserInfo.accountBalance < transferDetails.transferAmount:
                  raise HTTPException(status_code= 403, detail = 'Insufficient funds')
            else:
                senderUserInfo.accountBalance -= transferDetails.transferAmount
                receiverUserInfo.accountBalance += transferDetails.transferAmount
                db.commit()
                return "Transfer funds completed successfully"
    
@router.post("/accountransfer",status_code=200)
def fundTransfer(accountTransfer:schema.accountTransfer,dependencies = Depends(authBearer.jwtBearer()),db:Session = Depends(get_db)):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token :
        raise HTTPException (status_code= 404, detail= 'User not logged in')
    
    userId = token.userId 
    if accountTransfer.fromAccountType != "Saving" and accountTransfer.fromAccountType != 'Checking':
        raise HTTPException(status_code=404,detail="Account type does not exist")
    userInfo = db.query(models.UserInformation).filter(models.UserInformation.custId==userId,models.UserInformation.accountType == accountTransfer.fromAccountType).first()
    if not userInfo:
        raise HTTPException(status_code= 401, detail = 'Account needs to be updated by Bank Employee with User Information')
    
    receiverInfo =  db.query(models.UserInformation).filter(models.UserInformation.accountNumber==accountTransfer.toAccountNumber,models.UserInformation.routingNumber == accountTransfer.toRoutingNumber).first()

    if userInfo.accountBalance < accountTransfer.transferBalance : 
        raise HTTPException(status_code= 403, detail = 'Insufficient funds')

    receiverInfo.accountBalance+= accountTransfer.transferBalance
    userInfo.accountBalance -= accountTransfer.transferBalance
    db.commit()
    return "Fund Transfer Completed Successfully"




            
        
        


        

    







    







