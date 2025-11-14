from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

# =============================
# Base Schema (shared fields)
# =============================
class OrdersBase(BaseModel):
    distributer_id: int=0
    party_id: int
 
    remarks: Optional[str] = None


# =============================
# Create Schema (input)
# =============================
class OrdersCreate(OrdersBase):
    created_at: Optional[datetime] = None
    product_ready_date: Optional[datetime] = None


# =============================
# Update Schema (input)
# =============================
class OrdersUpdate(OrdersBase):
    updated_at: Optional[datetime] = None


# =============================
# Response Schema (output)
# =============================


class OrdersResponse(OrdersBase):
    id: int
    created_at: datetime
    updated_at: datetime
    distributer_name: Optional[str] = None
    party_name: Optional[str] = None

    class Config:
        from_attributes = True  # For ORM compatibility


# =============================
class OrdersUpdateStatus(BaseModel):
    status: str  # ready, arrived, received

    updated_at: Optional[datetime] = None

class OrderItemsBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: int
    discount: Optional[int] = 0
    paid_status: str  # cash, credit, etc.
    paid_amount: int

# =============================
# Create Schema (input)
# =============================
# =============================

class OrderItemsCreate(BaseModel):
    items: List[OrderItemsBase]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  

# =============================
# Response Schema (output)
# =============================

class OrderItemsResponse(OrderItemsBase):
    id: int
    total_item_price: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For ORM compatibility



