from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services

router = APIRouter(prefix="/distributer_products", tags=["Distributer Products"])
@router.post('/create', response_model=APIResponse[schemas.DistributerProducts])
def create_distributer_product(distributer_product:schemas.DistributerProductsCreate,db: Session = Depends(get_db)):
    res = services.create_distributer_product(distributer_product,db)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer Product not found")
    return APIResponse(data=res ,message="Distributer Product created successfully")    

@router.get('/', response_model=APIResponse[List[schemas.DistributerProducts]])
def get_distributer_products(db: Session = Depends(get_db)):
    res = services.get_distributer_products(db)
    return APIResponse(data=res ,message="Distributer Products fetched successfully")

@router.get('/{distributer_product_id}', response_model=APIResponse[schemas.DistributerProducts])
def get_distributer_product_by_id(distributer_product_id:int, db: Session = Depends(get_db)):
    res = services.get_distributer_product_by_id(db,distributer_product_id)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer Product not found")
    return APIResponse(data=res ,message="Distributer Product fetched successfully")

@router.get('/by_distributer/{distributer_id}', response_model=APIResponse[List[schemas.DistributerProducts]])
def get_distributer_products_by_distributer_id(distributer_id:int, db: Session = Depends(get_db)):
    res = services.distributer_product_by_distributer_id(distributer_id, db)
    if not res:
        return APIResponse(data =[] , message="Distributer Products not found")
    return APIResponse(data=res ,message="Distributer Products fetched successfully")

@router.put('/{distributer_product_id}', response_model=APIResponse[schemas.DistributerProducts])
def update_distributer_product(distributer_product_id:int, distributer_product:schemas.DistributerProductsUpdate, db: Session = Depends(get_db)):
    res = services.update_distributer_product(db,distributer_product_id,distributer_product)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer Product not found")
    return APIResponse(data=res ,message="Distributer Product updated successfully")

@router.delete('/{distributer_product_id}', response_model=APIResponse[schemas.DistributerProducts])
def delete_distributer_product(distributer_product_id:int, db: Session = Depends(get_db)):
    res = services.delete_distributer_product(db,distributer_product_id)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer Product not found")
    return APIResponse(data=res ,message="Distributer Product deleted successfully")
