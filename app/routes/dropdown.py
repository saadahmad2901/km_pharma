from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models
from app.schemas import DropDownSchema
from app import utils
from app.schemas.distributers import Distributers
import app.data as data 



router = APIRouter(prefix="/dropdowns", tags=["Dropdowns"])
@router.get("/users", response_model=List[DropDownSchema])
def users_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.Users, "id", "username")

@router.get("/user-roles", response_model=List[DropDownSchema])
def user_roles_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.UserRoles, "id", "role")

@router.get("/distributers")
def distributers_dropdown(db: Session = Depends(get_db)):
    db_rec = db.query(models.Distributers).all()
    
    result = []  # <- Store all dropdown items here

    for rec in db_rec:
        user = db.query(models.Users).filter(models.Users.id == rec.user_id).first()
        distributer_name = user.fullname if user else "Unknown"

        result.append({
            "label": distributer_name,
            "value": rec.id
        })

    return result



@router.get("/parties", response_model=List[DropDownSchema])
def parties_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.Parties, "id", "name")

@router.get("/suppliers", response_model=List[DropDownSchema])
def suppliers_dropdown(db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.Supplier, "id", "name")


@router.get("/veternary-products", response_model=List[DropDownSchema])
def veternary_products_dropdown(search: str = Query(None), db: Session = Depends(get_db)):
    return utils.get_dropdown_options(db, models.VeterinaryProduct, "id", "name")

# @router.get("/distributer-order-status",response_model=List[DropDownSchema])
# def 
@router.get("/payment-method")
def payment_method(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.payment_method, "value", "label", search=search)

@router.get("/payment-status")
def payment_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.payment_status, "value", "label", search=search)

@router.get("/order-distributer-status")
def order_distributer_status(search: str = Query(None)):    
    return utils.get_json_dropdown_options(data.order_distributer_status, "value", "label", search=search)
