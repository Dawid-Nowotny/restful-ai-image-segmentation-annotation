try:
    from database import SessionLocal
except ModuleNotFoundError:
    from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()