from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import APIResponse
from app.db import get_db
from app import models
from app import schemas
from app import services
from app.user_utils import get_current_user

router = APIRouter(prefix="/orders", tags=["Distributer Orders"])
@router.post("/", response_model=APIResponse[schemas.OrdersCreate]
             )
def create_distributer_order(
    order: schemas.OrdersCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_order = services.create_order(db, order, user)
    return APIResponse(success=True, data=db_order,message="Order created successfully")

@router.get("/", response_model=APIResponse[List[schemas.OrdersResponse]])
def get_distributer_orders(
   
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    orders = services.get_orders(db,user)
    return APIResponse(success=True, data=orders, message="Orders retrieved successfully")

@router.get("/{order_id}", response_model=APIResponse[schemas.OrdersResponse])
def get_distributer_order(
    order_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_order = services.get_order(db, order_id=order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return APIResponse(success=True, data=db_order, message="Order retrieved successfully")


@router.put("/{order_id}", response_model=APIResponse[schemas.OrdersUpdate])
def update_distributer_order(
    order_id: int,
    order: schemas.OrdersUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)

):
    db_order = services.update_order(db, order_id=order_id, order=order, user=user)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return APIResponse(success=True, data=db_order)

@router.delete("/{order_id}", response_model=APIResponse[None])
def delete_distributer_order(
    order_id: int,
    db: Session = Depends(get_db),
):
    success = services.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return APIResponse(success=True, data=None)

@router.patch("/{order_id}/status", response_model=APIResponse[schemas.OrdersUpdateStatus])
def update_distributer_order_status(
    order_id: int,
    status_update: schemas.OrdersUpdateStatus,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_order = services.update_order_status(db, order_id=order_id, status_update=status_update, user=user)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return APIResponse(success=True, data=db_order)

@router.post("/{order_id}/items-make-bill", response_model=APIResponse[schemas.OrderItemsCreate])
def create_order_item_and_make_bill(
    order_id: int,
    item: schemas.OrderItemsCreate,
    db: Session = Depends(get_db),
):
    db_item = services.create_order_item_and_make_bill(
        db, order_id=order_id, item=item
    )
    return APIResponse(
        success=True,
        data=db_item,
        message="Order items created and bill generated successfully"
    )

@router.get("/items-bill_by_order_id/{order_id}", response_model=APIResponse[schemas.OrderDetail])
def get_order_items(
    order_id: int,
    db: Session = Depends(get_db),
):
    items = services.get_order_items_bill_by_ordder_id(db, order_id=order_id)
    return APIResponse(
        success=True,
        data=items,
        message="Order items retrieved successfully"
    )
@router.put("/items-update/{item_id}", response_model=APIResponse[schemas.updateOrderItem])
def update_order_item(
    item_id: int,
    item: schemas.updateOrderItem,
    db: Session = Depends(get_db),
):
    db_item = services.update_order_item(
        db, item_id=item_id, item=item
    )
    if not db_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    return APIResponse(
        success=True,
        data=db_item,
        message="Order item updated successfully"
    )