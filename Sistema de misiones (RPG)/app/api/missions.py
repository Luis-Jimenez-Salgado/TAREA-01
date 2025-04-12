from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import mission_service
from app.schemas.mission import Mission, MissionCreate
from app.database import get_db

router = APIRouter(prefix="/misiones")

@router.post("/", response_model=Mission)
def create_mission(mission: MissionCreate, db: Session = Depends(get_db)):
    return mission_service.create_mission(db, mission)

@router.get("/", response_model=list[Mission])
def read_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return mission_service.get_missions(db, skip=skip, limit=limit)

@router.get("/{mission_id}", response_model=Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = mission_service.get_mission(db, mission_id)
    if mission is None:
        raise HTTPException(status_code=404, detail="Misión no encontrada")
    return mission