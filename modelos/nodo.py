from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime


class EstadoNodo(enum.Enum):
    ACTIVO   = "ACTIVO"    # SQL: ENUM('ACTIVO','INACTIVO','ERROR')
    INACTIVO = "INACTIVO"
    ERROR    = "ERROR"


class Nodo(Base):
    __tablename__ = "nodos"

    id_nodo          = Column(Integer, primary_key=True, autoincrement=True)
    identificador    = Column(String(100), unique=True, nullable=False)  # era 'nombre'
    direccion_red    = Column(String(100), nullable=False)               # era 'direccion_ip'
    puerto_pyro5     = Column(Integer, nullable=False)                   # era 'puerto'
    estado           = Column(Enum(EstadoNodo), default=EstadoNodo.ACTIVO, server_default="ACTIVO")
    ultima_actividad = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    trabajos_activos = Column(Integer, default=0)                        # era 'carga_actual'

    imagenes = relationship("Imagen", back_populates="nodo")
    logs     = relationship("LogEjecucion", back_populates="nodo")