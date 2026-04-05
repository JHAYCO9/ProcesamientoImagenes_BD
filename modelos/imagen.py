from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class EstadoImagen(enum.Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    LISTO = "listo"
    ERROR = "error"

class Imagen(Base):
    __tablename__ = "imagenes"
    
    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    id_lote = Column(Integer, ForeignKey("solicitudes_lote.id_lote"), nullable=False)
    id_nodo = Column(Integer, ForeignKey("nodos.id_nodo"), nullable=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_original = Column(String(512), nullable=False)
    ruta_resultado = Column(String(512), nullable=True)
    formato_original = Column(String(20), nullable=False)
    formato_resultado = Column(String(20), nullable=True)
    estado = Column(Enum(EstadoImagen), default=EstadoImagen.PENDIENTE)
    fecha_recepcion = Column(DateTime, default=datetime.utcnow)
    fecha_conversion = Column(DateTime, nullable=True)
    tamano_bytes = Column(Integer, default=0)
    mensaje_error = Column(Text, nullable=True)
    
    lote = relationship("SolicitudLote", back_populates="imagenes")
    nodo = relationship("Nodo", back_populates="imagenes")
    transformaciones = relationship("Transformacion", back_populates="imagen")
    logs = relationship("LogEjecucion", back_populates="imagen")
    
    def get_nodo(self):
        return self.nodo
    
    def get_transformaciones(self):
        return self.transformaciones
    
    def agregar_transformacion(self, transformacion):
        self.transformaciones.append(transformacion)
    
    def aplicar_transformacion(self, transformacion):
        self.agregar_transformacion(transformacion)
    
    def set_resultado(self, nodo, formato):
        self.nodo = nodo
        self.formato_resultado = formato
        self.ruta_resultado = f"resultados/{self.id_imagen}_{self.nombre_archivo}.{formato}"
        self.estado = EstadoImagen.LISTO
        self.fecha_conversion = datetime.utcnow()