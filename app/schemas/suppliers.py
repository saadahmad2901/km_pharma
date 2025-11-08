from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class SuppliersBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class SuppliersCreate(SuppliersBase):
    created_at: Optional[datetime] = None


class SuppliersUpdate(SuppliersBase):
    updated_at: Optional[datetime] = None


class Suppliers(SuppliersBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # ✅ Automatically fix invalid datetime strings
    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def fix_datetime_format(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "T")  # Replace space with T
            if v.endswith("+05"):    # Add missing :00 in timezone
                v += ":00"
        return v

    class Config:
        orm_mode = True
