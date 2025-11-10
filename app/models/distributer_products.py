from app.db import Base
from sqlalchemy import Column, Integer, String,ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import distributers, VeterinaryProduct

class DistributerProducts(Base):
    __tablename__ = 'distributer_products'

    id = Column(Integer, primary_key=True, index=True)
    distributer_id = Column(ForeignKey('distributers.id'), nullable=False)
    product_id = Column(ForeignKey('veterinary_products.id'), nullable=False)
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)

    distributer = relationship("Distributers", back_populates="products")
    product = relationship("VeterinaryProduct", back_populates="distributer_products")