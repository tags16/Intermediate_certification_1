import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from dotenv import load_dotenv
load_dotenv()

Base = declarative_base()

DATABASE = {
    "drivername": "postgres",
    "host": os.getenv('PG_HOST'),
    "port": os.getenv('PG_PORT'),
    "username": os.getenv('PG_USER'),
    "password": os.getenv('PG_PASSWORD'),
    "database": os.getenv('PG_NAME'),
}
DATABASE_URL = f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_NAME')}"

def db_connect() -> Engine:
    return create_engine(DATABASE_URL, encoding="utf8", echo=False)


