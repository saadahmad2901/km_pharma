from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import join
from app import schemas, models
from typing import List, Optional

from app.models import user
from app.routes.distributer_orders import get_distributer_order


def create_order(db: Session, order: schemas.OrdersCreate, user) -> schemas.OrdersCreate:
    print("-----------user in service:", user.id)
    # print("-------------------------------",user.__dict__)
    distributer_id = db.query(models.Distributers).filter(models.Distributers.user_id == user.id).first().id
    print("-----------distributer_id in service:", distributer_id)
    order.distributer_id = distributer_id



    db_order = models.Orders(**order.dict())  # ✅ use class, not module
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return order


def get_orders(
    db: Session,
    user
) -> List[schemas.OrdersResponse]:
    user_id = user.id
    distributer = db.query(models.Distributers).filter(models.Distributers.user_id == user_id).first()
    print("-----------distributer in service:", distributer.id)
    records = (
        db.query(
            models.Orders.id,
            models.Orders.distributer_id,
            models.Orders.party_id,
            models.Orders.status,
            models.Orders.product_ready_date,
            models.Orders.product_arrived_date,
            models.Orders.product_received_date,
            models.Orders.remarks,
            models.Orders.created_at,
            models.Orders.updated_at,
            models.Users.fullname.label("distributer_name"),
            models.Parties.name.label("party_name"),
        )
        .join(
            models.Distributers,
            models.Orders.distributer_id == models.Distributers.id,
        )
        .join(
            models.Users,
            models.Distributers.user_id == models.Users.id
        )
        .join(
            models.Parties,
            models.Orders.party_id == models.Parties.id,
        ).filter(models.Distributers.id == distributer.id).all()
    )

    return [
        schemas.OrdersResponse(
            id=r.id,
            distributer_id=r.distributer_id,
            party_id=r.party_id,
            status=r.status,
            product_ready_date=r.product_ready_date,
            product_arrived_date=r.product_arrived_date,
            product_received_date=r.product_received_date,
            remarks=r.remarks,
            created_at=r.created_at,
            updated_at=r.updated_at,
            distributer_name=r.distributer_name,
            party_name=r.party_name,
        )
        for r in records
    ]

def get_order(
    db: Session, order_id: int
) -> Optional[schemas.OrdersResponse]:
    r = (
        db.query(
            models.Orders.id,
            models.Orders.distributer_id,
            models.Orders.party_id,
            models.Orders.status,
            models.Orders.product_ready_date,
            models.Orders.product_arrived_date,
            models.Orders.product_received_date,
            models.Orders.remarks,
            models.Orders.created_at,
            models.Orders.updated_at,
            models.Users.fullname.label("distributer_name"),
            models.Parties.name.label("party_name"),
        )
        .join(
            models.Distributers,
            models.Orders.distributer_id == models.Distributers.id,
        )
        .join(
            models.Users,
            models.Distributers.user_id == models.Users.id
        )
        .join(
            models.Parties,
            models.Orders.party_id == models.Parties.id,
        )
        .filter(models.Orders.id == order_id)
        .first()
    )

    if r is None:
        return None

    return schemas.OrdersResponse(
        id=r.id,
        distributer_id=r.distributer_id,
        party_id=r.party_id,
        status=r.status,
        product_ready_date=r.product_ready_date,
        product_arrived_date=r.product_arrived_date,
        product_received_date=r.product_received_date,
        remarks=r.remarks,
        created_at=r.created_at,
        updated_at=r.updated_at,
        distributer_name=r.distributer_name,
        party_name=r.party_name,
    )

def update_order(
    db: Session, order_id: int, order: schemas.OrdersUpdate, user
) -> Optional[schemas.OrdersUpdate]:
    distributer_id = db.query(models.Distributers).filter(models.Distributers.user_id == user.id).first().id
    order.distributer_id = distributer_id

    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not db_order:
        return None

    for key, value in order.dict(exclude_unset=True).items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return order

def delete_order(
    db: Session, order_id: int
) -> bool:
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not db_order:
        return False

    db.delete(db_order)
    db.commit()
    return True

def update_order_status(
    db: Session, order_id: int, status_update: schemas.OrdersUpdateStatus, user
) -> Optional[schemas.OrdersUpdateStatus]:
    db_order = db.query(models.Orders).filter(models.Orders.id == order_id).first()
    if not db_order:
        return None
    if status_update.status =="arrived":
        db_order.product_arrived_date =  datetime.utcnow()
        db_order.status = "arrived"
    elif status_update.status =="received":
        db_order.product_received_date =  datetime.utcnow()
        db_order.status = "received"

    db.commit()
    db.refresh(db_order)
    return status_update




def create_order_item_and_make_bill(
    db: Session, order_id: int, item: schemas.OrderItemsCreate
):

    saved_items = []

    for i in item.items:

        # Check if product already exists for this order
        existing_item = (
            db.query(models.OrderItems)
            .filter(
                models.OrderItems.order_id == order_id,
                models.OrderItems.product_id == i.product_id
            )
            .first()
        )

        if existing_item:
            # Update quantity (add)
            existing_item.quantity += i.quantity  
            existing_item.unit_price = i.unit_price
            existing_item.discount = i.discount
            existing_item.paid_status = i.paid_status
            existing_item.paid_amount = i.paid_amount
            existing_item.updated_at = datetime.utcnow()

            saved_items.append(existing_item)

        else:
            # Insert new order item
            new_item = models.OrderItems(
                order_id=order_id,
                product_id=i.product_id,
                quantity=i.quantity,
                unit_price=i.unit_price,
                discount=i.discount,
                paid_status=i.paid_status,
                paid_amount=i.paid_amount,
                created_at=item.created_at or datetime.utcnow()
            )

            db.add(new_item)
            saved_items.append(new_item)

    db.commit()

    # Refresh all saved or updated items
    for si in saved_items:
        db.refresh(si)

    return item

