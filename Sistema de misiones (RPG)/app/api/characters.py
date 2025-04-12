from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import character_service, queue_service
from app.schemas.character import Character, CharacterCreate
from app.database import get_db

router = APIRouter(prefix="/personajes")

@router.post("/", response_model=Character)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    return character_service.create_character(db, character)

@router.post("/{character_id}/misiones/{mission_id}")
def accept_mission(character_id: int, mission_id: int, db: Session = Depends(get_db)):
    queue = queue_service.MissionQueue(db, character_id)
    return queue.enqueue(mission_id)

@router.post("/{character_id}/completar")
def complete_mission(character_id: int, db: Session = Depends(get_db)):
    queue = queue_service.MissionQueue(db, character_id)
    completed_mission = queue.dequeue()
    
    if not completed_mission:
        raise HTTPException(status_code=404, detail="No hay misiones pendientes")
    
    character = character_service.get_character(db, character_id)
    character.xp += completed_mission.mission.xp_reward
    db.commit()
    
    return {"message": "Misión completada", "xp_earned": completed_mission.mission.xp_reward}

@router.get("/{character_id}/misiones")
def list_missions(character_id: int, db: Session = Depends(get_db)):
    queue = queue_service.MissionQueue(db, character_id)
    return {
        "current_mission": queue.first(),
        "pending_missions_count": queue.size()
    }