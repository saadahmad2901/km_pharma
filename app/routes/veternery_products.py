from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/veterinary-products", tags=["Veterinary Products"])
@router.get('/', response_model=APIResponse[List[schemas.VeterinaryProduct]])
def get_veterinary_products(db: Session = Depends(get_db)):
    products = services.get_veterinary_products(db)
    print("products", products)
    return APIResponse(success=True, data=products, message="Veterinary Products fetched successfully")

@router.get('/{product_id}', response_model=APIResponse[schemas.VeterinaryProduct])
def get_veterinary_product(product_id: int, db: Session = Depends(get_db)):
    product = services.get_veterinary_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Veterinary Product not found")
    return APIResponse(data=product)

@router.post('/', response_model=APIResponse[schemas.VeterinaryProduct])
def create_veterinary_product(product: schemas.VeterinaryProductCreate, db: Session = Depends(get_db)):
    db_supplier = services.get_supplier_by_id(db, product.supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=400, detail="Invalid supplier ID")
    new_product = services.create_veterinary_product(db, product)
    return APIResponse(data=new_product)

@router.put('/{product_id}', response_model=APIResponse[schemas.VeterinaryProduct])
def update_veterinary_product(product_id: int, product: schemas.VeterinaryProductUpdate, db: Session = Depends(get_db)):
    db_product = services.get_veterinary_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Veterinary Product not found")
    updated_product = services.update_veterinary_product(db, product_id, product)
    return APIResponse(data=updated_product)

@router.patch('/{product_id}/update-price', response_model=APIResponse[schemas.VeterinaryProduct])
def update_veterinary_product_price(product_id: int, price: schemas.UpdatePriceVeterinaryProduct, db: Session = Depends(get_db)):
    db_product = services.get_veterinary_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Veterinary Product not found")
    updated_product = services.update_veterinary_product_price(db, product_id, price)
    return APIResponse(data=updated_product)

@router.delete('/{product_id}', response_model=APIResponse[schemas.VeterinaryProduct])
def delete_veterinary_product(product_id: int, db: Session = Depends(get_db)):
    db_product = services.get_veterinary_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Veterinary Product not found")
    deleted_product = services.delete_veterinary_product(db, product_id)
    return APIResponse(data=deleted_product)
