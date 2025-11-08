from sqlalchemy.orm import Session
from app import schemas, models
from typing import List

def get_suppliers(db: Session) -> List[schemas.Suppliers]:
    return db.query(models.Supplier).all()

def get_supplier_by_id(db: Session, supplier_id: int) -> models.Supplier:
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()

def create_supplier(supplier: schemas.SuppliersCreate, db: Session) -> models.Supplier:
    db_supplier = models.Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, supplier_id: int, supplier: schemas.SuppliersUpdate) -> models.Supplier:
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if db_supplier:
        for key, value in supplier.dict().items():
            setattr(db_supplier, key, value)
        db.commit()
        db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int) -> models.Supplier:
    db_supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if db_supplier:
        db.delete(db_supplier)
        db.commit()
    return db_supplier

