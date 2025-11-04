from app.db import Base
from sqlalchemy import Column, Integer, String
from datetime import datetime

class UserRoles(Base):
    __tablename__ = 'user_roles'


    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False)
