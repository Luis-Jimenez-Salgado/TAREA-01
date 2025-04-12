from sqlalchemy.orm import Session
from app.models import CharacterMission

class MissionQueue:
    def __init__(self, db: Session, character_id: int):
        self.db = db
        self.character_id = character_id
    
    def enqueue(self, mission_id: int):
        last_position = self.db.query(CharacterMission.queue_position)\
            .filter(CharacterMission.character_id == self.character_id)\
            .order_by(CharacterMission.queue_position.desc())\
            .first()
        
        new_position = 1 if last_position is None else last_position[0] + 1
        
        new_mission = CharacterMission(
            character_id=self.character_id,
            mission_id=mission_id,
            status="pending",
            queue_position=new_position
        )
        
        self.db.add(new_mission)
        self.db.commit()
        return new_mission
    
    def dequeue(self):
        mission = self.db.query(CharacterMission)\
            .filter(
                CharacterMission.character_id == self.character_id,
                CharacterMission.status == "pending"
            )\
            .order_by(CharacterMission.queue_position.asc())\
            .first()
        
        if mission:
            mission.status = "completed"
            self.db.commit()
            self._reorganize_queue()
            
        return mission
    
    def first(self):
        return self.db.query(CharacterMission)\
            .filter(
                CharacterMission.character_id == self.character_id,
                CharacterMission.status == "pending"
            )\
            .order_by(CharacterMission.queue_position.asc())\
            .first()
    
    def is_empty(self):
        return self.size() == 0
    
    def size(self):
        return self.db.query(CharacterMission)\
            .filter(
                CharacterMission.character_id == self.character_id,
                CharacterMission.status == "pending"
            )\
            .count()
    
    def _reorganize_queue(self):
        pending_missions = self.db.query(CharacterMission)\
            .filter(
                CharacterMission.character_id == self.character_id,
                CharacterMission.status == "pending"
            )\
            .order_by(CharacterMission.queue_position.asc())\
            .all()
        
        for index, mission in enumerate(pending_missions, start=1):
            mission.queue_position = index
        
        self.db.commit()