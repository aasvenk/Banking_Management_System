from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from DB.database import Base


class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True,index= True)
    title = Column(String)
    Author = Column(String)
    description = Column(String)
    rating = Column(Integer)
    

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

