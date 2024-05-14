from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#from .config import SQLALCHEMY_DATABASE_URL

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/raisa"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()