from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class EstadoNodo(enum.Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class Nodo(Base):
    __tablename__ = "nodos"
    
    id_nodo = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    direccion_ip = Column(String(45), nullable=False)
    puerto = Column(Integer, default=5000)
    estado = Column(Enum(EstadoNodo), default=EstadoNodo.ACTIVO)
    ultimo_latido = Column(DateTime, default=datetime.utcnow)
    capacidad_maxima = Column(Integer, default=10)
    carga_actual = Column(Integer, default=0)
    
    imagenes = relationship("Imagen", back_populates="nodo")
    logs = relationship("LogEjecucion", back_populates="nodo")