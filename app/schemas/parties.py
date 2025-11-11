from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime


class PartiesBase(BaseModel):
    name: str
    email: str
    phone: str
    adress: str
    distributer_id: int


class PartiesCreate(PartiesBase):
    created_at: Optional[datetime] = None


class PartiesUpdate(PartiesBase):
    updated_at: Optional[datetime] = None


class Parties(PartiesBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PartiesOut(PartiesBase):
    id: int
    distributer_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def fix_datetime_format(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "T")
            if v.endswith("+00") or v.endswith("+05"):
                v += ":00"
        return v

    class Config:
        orm_mode = True
