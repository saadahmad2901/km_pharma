from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class DistributerProductsBase(BaseModel):
    distributer_id: int
    product_id: int

class DistributerProductsCreate(DistributerProductsBase):
    created_at: Optional[datetime] = None

class DistributerProductsUpdate(DistributerProductsBase):
    updated_at: Optional[datetime] = None

class DistributerProducts(DistributerProductsBase):
    id: int
    product_name: Optional[str] = None
    distributer_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None




    # ✅ Automatically fix invalid datetime strings before parsing
    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def fix_datetime_format(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "T")
            # Fix missing colon in timezone (e.g., +00 → +00:00, +05 → +05:00)
            if v.endswith("+00") or v.endswith("+05"):
                v += ":00"
        return v

    class Config:
        orm_mode = True