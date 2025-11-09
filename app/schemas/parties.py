from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime


class PartiesBase(BaseModel):
    name: str
    email: str
    phone: str
    adress: str


class PartiesCreate(PartiesBase):
    created_at: Optional[datetime] = None


class PartiesUpdate(PartiesBase):
    updated_at: Optional[datetime] = None


class Parties(PartiesBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # ✅ Automatically fix invalid datetime strings before parsing
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
