from app.db import Base
from sqlalchemy import Column, Integer, String,ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import distributers, VeterinaryProduct

class DistributerOrders(Base):
    __tablename__ = 'distributer_orders'

    id = Column(Integer, primary_key=True, index=True)
    distributer_id = Column(ForeignKey('distributers.id'), nullable=False)
    product_id = Column(ForeignKey('veterinary_product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    order_details = Column(Text, nullable=False)    
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)

    distributer = relationship("Distributers", back_populates="orders")
