from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

def get_user_roles(db: Session) -> List[schemas.UserRoles]:
    return db.query(models.UserRoles).all()

def create_user_role(db: Session, role: schemas.UserRolesCreate) -> models.UserRoles:
    db_role = models.UserRoles(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_user_role(db: Session, role_id: int, role: schemas.UserRolesUpdate) -> models.UserRoles:
    db_role = db.query(models.UserRoles).filter(models.UserRoles.id == role_id).first()
    if db_role:
        for key, value in role.dict().items():
            setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role

def delete_user_role(db: Session, role_id: int) -> models.UserRoles:
    db_role = db.query(models.UserRoles).filter(models.UserRoles.id == role_id).first()
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role