from pydantic import BaseModel
from typing import Optional

class CharacterBase(BaseModel):
    name: str
    xp: Optional[int] = 0
    level: Optional[int] = 1

class CharacterCreate(CharacterBase):
    pass

class Character(CharacterBase):
    id: int
    
    class Config:
        from_attributes = True 