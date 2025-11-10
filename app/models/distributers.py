from app.db import Base
from sqlalchemy import Column, Integer, String,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class Distributers(Base):
    __tablename__ = 'distributers'


    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    adress = Column(String, nullable=False)
    area = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    products = relationship("DistributerProducts", back_populates="distributer")
# Distributers model
    user = relationship("Users", back_populates="distributers")

    
