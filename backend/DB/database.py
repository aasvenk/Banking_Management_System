from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  

POSTGRES_URL = os.getenv('POSTGRES_URL')
POSTGRES_USER_NM = os.getenv('POSTGRES_USER')
POSTGRES_PW = os.getenv('POSTGRES_PW')
POSTGRE_HOST = os.getenv('HOST')
POSTGRE_PORT = os.getenv('PORT')
POSTGRE_DB=os.getenv('POSTGRES_DB')

SQLALCHEMY_DATABASE_URL = POSTGRES_URL

#engine = create_engine('postgresql+psycopg2://postgres:Aashish%401997@127.0.0.1:5433/banking_system')
engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER_NM}:{POSTGRES_PW}@{POSTGRE_HOST}:{POSTGRE_PORT}/{POSTGRE_DB}')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
