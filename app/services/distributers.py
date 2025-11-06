from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

def create_distributer(distributer: schemas.DistributersCreate, db: Session) -> models.Distributers:
    db_distributer = models.Distributers(**distributer.dict())
    db.add(db_distributer)
    db.commit()
    db.refresh(db_distributer)
    return db_distributer

def get_distributers(db: Session) -> List[schemas.Distributers]:
    return db.query(models.Distributers).all()

def get_distributer_by_id(db: Session, distributer_id: int) -> models.Distributers:
    return db.query(models.Distributers).filter(models.Distributers.id == distributer_id).first()

def update_distributer(db: Session, distributer_id: int, distributer: schemas.DistributersUpdate) -> models.Distributers:
    db_distributer = db.query(models.Distributers).filter(models.Distributers.id == distributer_id).first()
    if db_distributer:
        for key, value in distributer.dict().items():
            setattr(db_distributer, key, value)
        db.commit()
        db.refresh(db_distributer)
    return db_distributer

def delete_distributer(db: Session, distributer_id: int) -> models.Distributers:
    db_distributer = db.query(models.Distributers).filter(models.Distributers.id == distributer_id).first()
    if db_distributer:
        db.delete(db_distributer)
        db.commit()
    return db_distributer

