from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models
from app.schemas import DropDownSchema
from app import utils
from app.schemas.distributers import Distributers


router = APIRouter(prefix="/dropdowns", tags=["Dropdowns"])

@router.get("/user-roles", response_model=List[DropDownSchema])
def user_roles_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.UserRoles, "role", "role")

@router.get("/distributers", response_model=List[DropDownSchema])
def distributers_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.Distributers, "id", "name")
