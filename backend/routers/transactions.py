from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session 
from DB import schema
from DB import models
from DB import database
from utils import authBearer
from uuid import UUID
from datetime import datetime


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
                senderStatement = models.SelfBankStatements(emailId=senderUserInfo.emailId,accountType="Saving", transactionType="Debit", amount=transferDetails.transferAmount,balance=senderUserInfo.accountBalance,timestamp=datetime.now())
                receiverStatement = models.SelfBankStatements(emailId=receiverUserInfo.emailId, accountType="Checking", transactionType="Credit", amount=transferDetails.transferAmount,balance= receiverUserInfo.accountBalance,timestamp=datetime.now())
                db.add(senderStatement)
                db.add(receiverStatement)
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
                senderStatement = models.SelfBankStatements(emailId=senderUserInfo.emailId,accountType="Checking", transactionType="Debit", amount=transferDetails.transferAmount,balance=senderUserInfo.accountBalance,timestamp=datetime.now())
                receiverStatement = models.SelfBankStatements(emailId=receiverUserInfo.emailId, accountType="Saving", transactionType="Credit", amount=transferDetails.transferAmount,balance= receiverUserInfo.accountBalance,timestamp=datetime.now())
                db.add(senderStatement)
                db.add(receiverStatement)
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
    if not receiverInfo:
        raise HTTPException(status_code=404,detail="Wrong Account number or routing Number")
    
    if userInfo.accountBalance < accountTransfer.transferBalance : 
        raise HTTPException(status_code= 403, detail = 'Insufficient funds')
    

    transferRequest = models.TransferRequest(
        fromAccountNumber=userInfo.accountNumber,
        toAccountNumber=accountTransfer.toAccountNumber,
        toRoutingNumber=accountTransfer.toRoutingNumber,
        amount=accountTransfer.transferBalance,
        approved=False  
    )

    db.add(transferRequest)
    db.commit()


@router.post("/approveTransfer/{requestId}",status_code=200)
def approveTransfer(requestId: UUID,dependencies = Depends(authBearer.jwtBearer()), db: Session = Depends(get_db)):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token :
        raise HTTPException (status_code= 404, detail= 'User not logged in')

    transferRequest = db.query(models.TransferRequest).filter(models.TransferRequest.id == requestId).first()
    if not transferRequest:
        raise HTTPException(status_code=404, detail="Transfer request not found")

    if transferRequest.approved:
        raise HTTPException(status_code=400, detail="Transfer request already approved")


    fromUser = db.query(models.UserInformation).filter(models.UserInformation.accountNumber == transferRequest.fromAccountNumber).first()
    toUser = db.query(models.UserInformation).filter(models.UserInformation.accountNumber == transferRequest.toAccountNumber, models.UserInformation.routingNumber == transferRequest.toRoutingNumber).first()

    fromUser.accountBalance -= transferRequest.amount
    toUser.accountBalance += transferRequest.amount
    transferRequest.approved = True
    db.commit()
    return {"message": "Transfer approved and completed"}


@router.get("/getSelfTransfers")
def getAllSelfTransfers(dependencies = Depends(authBearer.jwtBearer()), db: Session = Depends(get_db)):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token :
        raise HTTPException (status_code= 404, detail= 'User not logged in')
    userId=token.userId
    emailId = db.query(models.Users).filter(models.Users.id == userId).first().emailId
    transactions = db.query(models.SelfBankStatements).filter(models.SelfBankStatements.emailId ==emailId).all()
    userInfoList = []
    for transaction in transactions:
        transDict = {
        "transactionId": transaction.id,
        "emailId": transaction.emailId,
        "accountType": transaction.accountType,
        "transactionType": transaction.transactionType,
        "amount": transaction.amount,
        "Balance":transaction.balance,
        "timestamp": transaction.accountType
    }
        userInfoList.append(transDict)
    return  userInfoList


@router.delete("/deleteUser/{emailId}", status_code=200)
def delete_user(emailId: str, db: Session = Depends(get_db), dependencies= Depends(authBearer.jwtBearer())):
    token = db.query(models.TokenTable).filter(models.TokenTable.accessToken== dependencies).first()
    if not token :
        raise HTTPException (status_code= 404, detail= 'User not logged in')
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
        if not userInformationSavingQuery and not userInformationCheckingQuery:
            pass
        else: 
            if userInformationSavingQuery:
                transferRequestSavingQuery = db.query(models.TransferRequest).filter(models.TransferRequest.fromAccountNumber == userInformationSavingQuery.accountNumber).all()
                if not transferRequestSavingQuery:
                    pass
                else:
                    transferRequestResult = db.query(models.TransferRequest).filter(models.TransferRequest.fromAccountNumber == userInformationSavingQuery.accountNumber).delete()
                    db.commit()
            if userInformationCheckingQuery:
                transferRequestCheckingQuery = db.query(models.TransferRequest).filter(models.TransferRequest.fromAccountNumber == userInformationCheckingQuery.accountNumber).all()
                if not transferRequestCheckingQuery:
                    pass
                else:
                    transferRequestResult = db.query(models.TransferRequest).filter(models.TransferRequest.fromAccountNumber == userInformationCheckingQuery.accountNumber).delete()
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
        
