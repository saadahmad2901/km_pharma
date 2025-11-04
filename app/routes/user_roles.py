from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(prefix="/user-roles", tags=["User Roles"])
@router.get('/', response_model=List[schemas.UserRoles])
def read_user_roles(db: Session = Depends(get_db)):
    data = services.get_user_roles(db)
    return data
@router.post('/create', response_model=APIResponse[schemas.UserRoles])
def create_user_role(role:schemas.UserRolesCreate,db: Session = Depends(get_db)):
    res = services.create_user_role(db,role)
    if not res:
        raise HTTPException(status_code=404, detail="Role could not be created")
    return APIResponse(data=res ,message="User role created successfully")
@router.put('/update/{role_id}', response_model=APIResponse[schemas.UserRoles])
def update_user_role(role_id:int, role:schemas.UserRolesUpdate,db: Session = Depends(get_db)):
    res = services.update_user_role(db,role_id,role)
    if not res:
        raise HTTPException(status_code=404, detail="Role not found")
    return APIResponse(data=res ,message="User role updated successfully")
@router.delete('/delete/{role_id}', response_model=APIResponse[schemas.UserRoles])
def delete_user_role(role_id:int,db: Session = Depends(get_db)):
    res = services.delete_user_role(db,role_id)
    if not res:
        raise HTTPException(status_code=404, detail="Role not found")
    return APIResponse(data=res ,message="User role deleted successfully")

