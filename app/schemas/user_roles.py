from typing import Optional
from pydantic import BaseModel, validator

class UserRoles(BaseModel):
    id: int
    role: str

    class Config:
        orm_mode = True


class UserRolesCreate(BaseModel):
    role: str

    @validator('role')
    def capitalize_role(cls, v: str) -> str:
        return v.capitalize()  # Capitalize the string before saving

    class Config:
        orm_mode = True


class UserRolesUpdate(BaseModel):
    role: str

    @validator('role')
    def capitalize_role(cls, v: str) -> str:
        return v.capitalize()  # Capitalize the string before updating

    class Config:
        orm_mode = True
