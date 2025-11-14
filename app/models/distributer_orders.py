from app.db import Base
from sqlalchemy import Column, Integer, String,ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models import Distributers,VeterinaryProduct


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    distributer_id = Column(Integer, ForeignKey("distributers.id"), nullable=False)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False)
    product_ready_date = Column(DateTime, nullable=True)
    product_arrived_date = Column(DateTime, nullable=True)
    product_received_date = Column(DateTime, nullable=True)
    status = Column(String, default="ready")  # ready, arrived, received
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    distributer = relationship("Distributers")
    party = relationship("Parties")


class OrderItems(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("veterinary_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=True, default=0)
    paid_status = Column(String, nullable=False)  # cash, credit, etc.
    paid_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = relationship("Orders")
    product = relationship("VeterinaryProduct")
