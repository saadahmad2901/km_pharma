from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

class DistributersBase(BaseModel):
    name: str
    email: str
    phone: str
    adress: str
    area: str


class DistributersCreate(DistributersBase):
    created_at: Optional[datetime] = None


class DistributersUpdate(DistributersBase):
    updated_at: Optional[datetime] = None


class Distributers(DistributersBase):
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
