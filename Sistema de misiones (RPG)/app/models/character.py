from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    
    missions = relationship("CharacterMission", back_populates="character")