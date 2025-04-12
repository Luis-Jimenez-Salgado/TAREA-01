from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
from app.api import characters, missions

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(characters.router)
app.include_router(missions.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()