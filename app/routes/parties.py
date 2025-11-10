from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services
from app.user_utils import get_current_user

router = APIRouter(prefix="/parties", tags=["Parties"])
@router.post('/create', response_model=APIResponse[schemas.Parties]
             )
def create_party(party:schemas.PartiesCreate,db: Session = Depends(get_db)
                 ):
    res = services.create_party(party,db)
    if not res:
        raise HTTPException(status_code=404, detail="Party not found")
    return APIResponse(data=res ,message="Party created successfully")
@router.get('/', response_model=APIResponse[List[schemas.Parties]])
@router.get('/', response_model=APIResponse[List[schemas.Parties]])
def get_parties(db: Session = Depends(get_db)):
    res = services.get_parties(db)
    return APIResponse(data=res, message="Parties retrieved successfully")
@router.get('/{party_id}', response_model=APIResponse[schemas.Parties])
def get_party_by_id(party_id:int, db: Session = Depends(get_db)):
    res = services.get_party_by_id(db,party_id)
    if not res:
        raise HTTPException(status_code=404, detail="Party not found")
    return APIResponse(data=res ,message="Party fetched successfully")
@router.put('/{party_id}', response_model=APIResponse[schemas.Parties])
def update_party(party_id:int, party:schemas.PartiesUpdate, db: Session = Depends(get_db)):
    res = services.update_party(db,party_id,party)
    if not res:
        raise HTTPException(status_code=404, detail="Party not found")
    return APIResponse(data=res ,message="Party updated successfully")
@router.delete('/{party_id}', response_model=APIResponse[schemas.Parties])
def delete_party(party_id:int, db: Session = Depends(get_db)):
    res = services.delete_party(db,party_id)
    if not res:
        raise HTTPException(status_code=404, detail="Party not found")
    return APIResponse(data=res ,message="Party deleted successfully")