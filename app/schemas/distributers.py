from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from app.schemas import UserOut

class DistributersBase(BaseModel):
    user_id: int
    phone: str
    adress: str
    area: str


class DistributersCreate(DistributersBase):
    created_at: Optional[datetime] = None


class DistributersUpdate(BaseModel):
    phone: str
    adress: str
    area: str
    updated_at: Optional[datetime] = None


class Distributers(DistributersBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class DistributersOut(DistributersBase):
    id: int
    user: UserOut
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # ✅ Safely fix datetime strings and auto-convert to datetime object
    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def fix_datetime_format(cls, v):
            if isinstance(v, str):
                v = v.replace(" ", "T")
                # Fix missing colon in timezone (e.g. +00 → +00:00 or +05 → +05:00)
                if v.endswith("+00") or v.endswith("+05"):
                    v += ":00"
                # If it ends with 'Z' or already valid, leave it
            return v

    class Config:
            orm_mode = True