from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class EntidadBase(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    creado_en = Column(DateTime, default=datetime.utcnow)