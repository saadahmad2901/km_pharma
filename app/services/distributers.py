from sqlalchemy.orm import Session
from app import schemas, models
from typing import List
from sqlalchemy.orm import joinedload


def create_distributer(distributer: schemas.DistributersCreate, db: Session) -> bool:
    db_distributer = models.Distributers(**distributer.dict())
    db.add(db_distributer)
    db.commit()
    db.refresh(db_distributer)
    return True


def get_distributers(db: Session) -> List[schemas.DistributersOut]:
    # Use the relationship "user", not the column "user_id"
    distributers = db.query(models.Distributers).options(joinedload(models.Distributers.user)).all()
    return distributers



def get_distributer_by_id(db: Session, distributer_id: int) -> schemas.DistributersOut:
    return db.query(models.Distributers).options(joinedload(models.Distributers.user)).filter(models.Distributers.id == distributer_id).first()

def update_distributer(db: Session, distributer_id: int, distributer: schemas.DistributersUpdate) -> models.Distributers:
    db_distributer = db.query(models.Distributers).options(joinedload(models.Distributers.user)).filter(models.Distributers.id == distributer_id).first()
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

