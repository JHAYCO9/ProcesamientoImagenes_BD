from sqlalchemy import Column, Integer, ForeignKey, String, JSON, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime


class EstadoTransformacion(enum.Enum):
    PENDIENTE  = "PENDIENTE"   # SQL: ENUM('PENDIENTE','PROCESANDO','LISTO','ERROR')
    PROCESANDO = "PROCESANDO"
    LISTO      = "LISTO"
    ERROR      = "ERROR"


class TipoTransformacion(enum.Enum):
    GRISES             = "GRISES"
    REDIMENSIONAR      = "REDIMENSIONAR"
    RECORTAR           = "RECORTAR"
    ROTAR              = "ROTAR"
    REFLEJAR           = "REFLEJAR"
    DESENFOCAR         = "DESENFOCAR"
    PERFILAR           = "PERFILAR"
    BRILLO_CONTRASTE   = "BRILLO_CONTRASTE"
    MARCA_AGUA         = "MARCA_AGUA"
    CONVERSION_FORMATO = "CONVERSION_FORMATO"


class Transformacion(Base):
    __tablename__ = "transformaciones"

    id_transformacion = Column(Integer, primary_key=True, autoincrement=True)
    id_imagen         = Column(Integer, ForeignKey("imagenes.id_imagen"), nullable=False)
    tipo              = Column(Enum(TipoTransformacion), nullable=False)
    parametros        = Column(JSON, nullable=True)
    orden             = Column(Integer, default=0)
    estado            = Column(Enum(EstadoTransformacion), default=EstadoTransformacion.PENDIENTE)
    fecha_ejecucion   = Column(DateTime, nullable=True)

    imagen = relationship("Imagen", back_populates="transformaciones")