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


# @app.get("/")
# def read_api(db:Session = Depends(get_db)):
#     return db.query(models.Books).all()

# @app.post("/")
# def create_book(book: schema.Book,db:Session = Depends(get_db)):
#     book_model = models.Books()
#     book_model.title = book.title
#     book_model.Author = book.author
#     book_model.description = book.description
#     book_model.rating = book.rating
#     db.add(book_model)
#     db.commit()
    
    