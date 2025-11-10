from app.db import Base
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class VeterinaryProduct(Base):
    __tablename__ = "veterinary_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))  
    brand = Column(String(255))
    category = Column(String(100))
    composition = Column(Text)
    dosage_form = Column(String(100))
    pack_size = Column(String(100))
    species_targeted = Column(String(255))
    usage_instructions = Column(Text)
    withdrawal_period = Column(String(255), nullable=True)
    storage_conditions = Column(String(255), nullable=True)
    side_effects = Column(Text, nullable=True)
    buying_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    
    batch_no = Column(String(100), nullable=True)
    manufacture_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    remarks = Column(Text, nullable=True)

    # Relationship
    supplier = relationship("Supplier", back_populates="products")
    distributer_products = relationship("DistributerProducts", back_populates="product")

