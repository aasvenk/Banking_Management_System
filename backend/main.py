from fastapi import FastAPI,Depends
from DB import models
from DB import database
engine = database.engine
SessionLocal = database.SessionLocal
from pydantic import BaseModel,Field
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind= engine) # creates all tables if tables are not yet created when server is restarted.

def get_db(): 
    try :
        db= SessionLocal()
        yield db
    finally:
        db.close()

class Book(BaseModel): #Create Validations for the 
    title :str = Field(min_length = 1)
    author :str = Field(min_length = 1,max_length= 100)
    description : str = Field(min_length = 1,max_length = 100)
    rating : int = Field(gt = -1,lt=101)
    

@app.get("/")
def read_api(db:Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.post("/")
def create_book(book: Book,db:Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.Author = book.author
    book_model.description = book.description
    book_model.rating = book.rating
    db.add(book_model)
    db.commit()
    
    