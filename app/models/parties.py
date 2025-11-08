from app.db import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime

class Parties(Base):
    __tablename__ = 'parties'


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    adress = Column(String, nullable=False)
    created_at = Column(String, default=datetime.utcnow)
    updated_at = Column(String, default=datetime.utcnow, onupdate=datetime.utcnow)
    
