from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime


class EstadoLote(enum.Enum):
    PENDIENTE  = "PENDIENTE"    # SQL: ENUM('PENDIENTE','EN_PROCESO','COMPLETADO','ERROR')
    EN_PROCESO = "EN_PROCESO"
    COMPLETADO = "COMPLETADO"
    ERROR      = "ERROR"


class SolicitudLote(Base):
    __tablename__ = "solicitudes_lote"

    id_lote              = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario           = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    fecha_recepcion      = Column(DateTime, default=datetime.utcnow)
    estado               = Column(Enum(EstadoLote), default=EstadoLote.PENDIENTE)
    total_imagenes       = Column(Integer, default=0)
    imagenes_completadas = Column(Integer, default=0)

    usuario  = relationship("Usuario", back_populates="solicitudes")
    imagenes = relationship("Imagen", back_populates="lote")

    def get_progreso(self) -> float:
        if self.total_imagenes == 0:
            return 0.0
        return (self.imagenes_completadas / self.total_imagenes) * 100

    def agregar_imagen(self, imagen):
        self.imagenes.append(imagen)
        self.total_imagenes = len(self.imagenes)

    def esta_completo(self) -> bool:
        return self.imagenes_completadas >= self.total_imagenes and self.total_imagenes > 0