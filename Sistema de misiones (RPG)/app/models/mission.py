from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    xp_reward = Column(Integer, default=10)
    difficulty = Column(Enum("easy", "medium", "hard", name="difficulty_levels"))
    
class CharacterMission(Base):
    __tablename__ = "character_missions"
    
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    mission_id = Column(Integer, ForeignKey("missions.id"))
    status = Column(Enum("pending", "completed", name="mission_status"), default="pending")
    queue_position = Column(Integer)
    
    character = relationship("Character", back_populates="missions")
    mission = relationship("Mission")