from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime

# Base model shared by Create, Update, and Read models
class VeterinaryProductBase(BaseModel):
    name: str
    supplier_id: int
    brand: str
    category: str
    composition: str
    dosage_form: str
    pack_size: str
    species_targeted: str
    usage_instructions: str
    withdrawal_period: str
    storage_conditions: str
    side_effects: str
    buying_price: float
    selling_price: float
    batch_no: str
    manufacture_date: datetime
    expiry_date: datetime
    remarks: str


# Create model
class VeterinaryProductCreate(VeterinaryProductBase):
    created_at: Optional[datetime] = None

# Update model
class VeterinaryProductUpdate(VeterinaryProductBase):
    updated_at: Optional[datetime] = None

class UpdatePriceVeterinaryProduct(BaseModel):
    buying_price: float
    selling_price: float

# Read / Response model
class VeterinaryProduct(VeterinaryProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class VeterinaryProductResponse(VeterinaryProduct):
    supplier_name: Optional[str] = None


    # Automatically fix invalid datetime strings
    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def fix_datetime_format(cls, v):
        if isinstance(v, str):
            v = v.replace(" ", "T")  # Replace space with T
            if v.endswith("+05"):    # Add missing :00 in timezone
                v += ":00"
        return v

    class Config:
        from_attributes = True  # ✅ Correct Pydantic V2 ORM support
        orm_mode = True         # ✅ Correct Pydantic V1 ORM support