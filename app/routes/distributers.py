from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services

router = APIRouter(prefix="/distributers", tags=["Distributers"])
@router.post('/create', response_model=bool)
def create_distributer(distributer:schemas.DistributersCreate,db: Session = Depends(get_db)):
    res = services.create_distributer(distributer,db)
    
    return True

@router.get('/', response_model=APIResponse[List[schemas.DistributersOut]])
def get_distributers(db: Session = Depends(get_db)):
    res = services.get_distributers(db)
    return APIResponse(data=res ,message="Distributers fetched successfully")

@router.get('/{distributer_id}', response_model=APIResponse[schemas.DistributersOut])
def get_distributer_by_id(distributer_id:int, db: Session = Depends(get_db)):
    res = services.get_distributer_by_id(db,distributer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer not found")
    return APIResponse(data=res ,message="Distributer fetched successfully")

@router.put('/{distributer_id}', response_model=bool)
def update_distributer(distributer_id:int, distributer:schemas.DistributersUpdate, db: Session = Depends(get_db)):
    res = services.update_distributer(db,distributer_id,distributer)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer not found")
    return True

@router.delete('/{distributer_id}', response_model=bool)
def delete_distributer(distributer_id:int, db: Session = Depends(get_db)):
    res = services.delete_distributer(db,distributer_id)
    if not res:
        raise HTTPException(status_code=404, detail="Distributer not found")
    return True
