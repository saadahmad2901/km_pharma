from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])
@router.post('/create', response_model=APIResponse[schemas.Suppliers])
def create_supplier(supplier:schemas.SuppliersCreate,db: Session = Depends(get_db)):
    res = services.create_supplier(supplier,db)
    if not res:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return APIResponse(data=res ,message="Supplier created successfully")

@router.get('/', response_model=APIResponse[List[schemas.Suppliers]])
def get_suppliers(db: Session = Depends(get_db)):
    res = services.get_suppliers(db)
    
    return APIResponse(data=res ,message="Suppliers fetched successfully")

@router.get('/{supplier_id}', response_model=APIResponse[schemas.Suppliers])
def get_supplier_by_id(supplier_id:int, db: Session = Depends(get_db)):
    res = services.get_supplier_by_id(db,supplier_id)
    if not res:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return APIResponse(data=res ,message="Supplier fetched successfully")

@router.put('/{supplier_id}', response_model=APIResponse[schemas.Suppliers])
def update_supplier(supplier_id:int, supplier:schemas.SuppliersUpdate, db: Session = Depends(get_db)):
    res = services.update_supplier(db,supplier_id,supplier)
    if not res:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return APIResponse(data=res ,message="Supplier updated successfully")
@router.delete('/{supplier_id}', response_model=APIResponse[schemas.Suppliers])
def delete_supplier(supplier_id:int, db: Session = Depends(get_db)):
    res = services.delete_supplier(db,supplier_id)
    if not res:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return APIResponse(data=res ,message="Supplier deleted successfully")
