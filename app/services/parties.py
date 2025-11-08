from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

def get_parties(db: Session) -> List[schemas.Parties]:
    return db.query(models.Parties).all()

def get_party_by_id(db: Session, party_id: int) -> models.Parties:
    return db.query(models.Parties).filter(models.Parties.id == party_id).first()   

def create_party(party: schemas.PartiesCreate, db: Session) -> models.Parties:
    db_party = models.Parties(**party.dict())
    db.add(db_party)
    db.commit()
    db.refresh(db_party)
    return db_party

def update_party(db: Session, party_id: int, party: schemas.PartiesUpdate) -> models.Parties:
    db_party = db.query(models.Parties).filter(models.Parties.id == party_id).first()
    if db_party:
        for key, value in party.dict().items():
            setattr(db_party, key, value)
        db.commit()
        db.refresh(db_party)
    return db_party

def delete_party(db: Session, party_id: int) -> models.Parties:
    db_party = db.query(models.Parties).filter(models.Parties.id == party_id).first()
    if db_party:
        db.delete(db_party)
        db.commit()
    return db_party

