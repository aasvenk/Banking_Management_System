from fastapi import FastAPI,Depends
from DB import models
from DB import database
engine = database.engine
SessionLocal = database.SessionLocal
# from DB import schema
# from sqlalchemy.orm import Session
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind= engine) # creates all tables if tables are not yet created when server is restarted.

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message":"Hellu hope this works"}





    
    