from app.db import Base
from sqlalchemy import Column, DateTime, Integer, String
from datetime import datetime
from sqlalchemy.sql import func


class Parties(Base):
    __tablename__ = 'parties'


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    adress = Column(String, nullable=False)
    distributer_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
