from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime


class EstadoImagen(enum.Enum):
    PENDIENTE  = "PENDIENTE"   # SQL: ENUM('PENDIENTE','PROCESANDO','LISTO','ERROR')
    PROCESANDO = "PROCESANDO"
    LISTO      = "LISTO"
    ERROR      = "ERROR"


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen         = Column(Integer, primary_key=True, autoincrement=True)
    id_lote           = Column(Integer, ForeignKey("solicitudes_lote.id_lote"), nullable=False)
    id_nodo           = Column(Integer, ForeignKey("nodos.id_nodo"), nullable=True)
    nombre_archivo    = Column(String(255), nullable=False)
    ruta_original     = Column(String(500), nullable=False)
    ruta_resultado    = Column(String(500), nullable=True)
    formato_original  = Column(String(10), nullable=False)
    formato_resultado = Column(String(10), nullable=True)
    estado            = Column(Enum(EstadoImagen), default=EstadoImagen.PENDIENTE)
    fecha_recepcion   = Column(DateTime, default=datetime.utcnow)
    fecha_conversion  = Column(DateTime, nullable=True)
    tamano_bytes      = Column(Integer, nullable=True)
    # 'mensaje_error' eliminado — no existe en el SQL real

    lote             = relationship("SolicitudLote", back_populates="imagenes")
    nodo             = relationship("Nodo", back_populates="imagenes")
    transformaciones = relationship("Transformacion", back_populates="imagen")
    logs             = relationship("LogEjecucion", back_populates="imagen")

    def set_resultado(self, nodo, formato):
        self.nodo             = nodo
        self.formato_resultado = formato
        self.estado           = EstadoImagen.LISTO
        self.fecha_conversion = datetime.utcnow()