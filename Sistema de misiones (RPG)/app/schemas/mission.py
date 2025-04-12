from pydantic import BaseModel
from typing import Optional

class MissionBase(BaseModel):
    title: str
    description: Optional[str] = None
    xp_reward: int = 10
    difficulty: str = "easy"

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    
    class Config:
        from_attributes = True