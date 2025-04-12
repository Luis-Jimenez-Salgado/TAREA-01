from sqlalchemy.orm import Session
from app.models.character import Character
from app.schemas.character import CharacterCreate

def get_character(db: Session, character_id: int):
    return db.query(Character).filter(Character.id == character_id).first()

def create_character(db: Session, character: CharacterCreate):
    db_character = Character(**character.dict())
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character