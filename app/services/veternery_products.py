from sqlalchemy.orm import Session
from app import schemas, models
from typing import List


def get_veterinary_products(db: Session) -> List[schemas.VeterinaryProduct]:
    res =  db.query(models.VeterinaryProduct).all()

    print("test", res)
    return res

def get_veterinary_product_by_id(db: Session, product_id: int) -> models.VeterinaryProduct:
    return db.query(models.VeterinaryProduct).filter(models.VeterinaryProduct.id == product_id).first()

def create_veterinary_product(db: Session, product: schemas.VeterinaryProductCreate) -> models.VeterinaryProduct:
    db_product = models.VeterinaryProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
def get_veterinary_products_by_supplier(db: Session, supplier_id: int) -> List[schemas.VeterinaryProduct]:
    return db.query(models.VeterinaryProduct).filter(models.VeterinaryProduct.supplier_id == supplier_id).all() 

def update_veterinary_product(db: Session, product_id: int, product: schemas.VeterinaryProductUpdate) -> models.VeterinaryProduct:
    db_product = db.query(models.VeterinaryProduct).filter(models.VeterinaryProduct.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def update_veterinary_product_price(db: Session, product_id: int, price: schemas.UpdatePriceVeterinaryProduct) -> models.VeterinaryProduct:
    db_product = db.query(models.VeterinaryProduct).filter(models.VeterinaryProduct.id == product_id).first()
    if db_product:
        db_product.buying_price = price.buying_price
        db_product.selling_price = price.selling_price
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_veterinary_product(db: Session, product_id: int) -> models.VeterinaryProduct:
    db_product = db.query(models.VeterinaryProduct).filter(models.VeterinaryProduct.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

