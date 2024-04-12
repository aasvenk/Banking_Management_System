from fastapi import FastAPI,Depends
from DB import models
from DB import database
engine = database.engine
SessionLocal = database.SessionLocal
# from DB import schema
# from sqlalchemy.orm import Session
from routers import auth,userInfo,transactions
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv() 

app = FastAPI()

models.Base.metadata.create_all(bind= engine) # creates all tables if tables are not yet created when server is restarted.

origins = os.getenv("FRONTEND_URL"),

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(userInfo.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return {"Message": "Please visit http://156.56.103.190/docs for all backend operations"}





    
    