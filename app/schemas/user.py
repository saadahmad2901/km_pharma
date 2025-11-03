from typing import Optional
from datetime import datetime, date, time
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    role: str  # changed from status → role

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    fullname: str
    email: str
    username: str
    password: str
    is_active: bool = True
    role: str = 'Admin'  # changed from status → role

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: str
    username: str
    password: str
    is_active: bool = True
    role: str = 'Admin'  # changed from status → role


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdatePassword(BaseModel):
    email: str
    password: str


class UserUpdateRole(BaseModel):  # renamed for clarity
    role: str  # changed from status → role


class UserOut(BaseModel):
    id: int
    fullname: str
    email: str
    username: str
    role: str  # changed from status → role
    is_active: bool

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

    class Config:
        orm_mode = True
