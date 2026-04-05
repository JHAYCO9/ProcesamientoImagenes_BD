from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class NivelLog(enum.Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    DEBUG = "debug"

class LogEjecucion(Base):
    __tablename__ = "logs_ejecucion"
    
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_imagen = Column(Integer, ForeignKey("imagenes.id_imagen"), nullable=True)
    id_nodo = Column(Integer, ForeignKey("nodos.id_nodo"), nullable=True)
    mensaje = Column(String(1000), nullable=False)
    nivel = Column(Enum(NivelLog), default=NivelLog.INFO)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    imagen = relationship("Imagen", back_populates="logs")
    nodo = relationship("Nodo", back_populates="logs")