from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

try:
    from config import SQLALCHEMY_DATABASE_URL
except ModuleNotFoundError:
    from .config import SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()