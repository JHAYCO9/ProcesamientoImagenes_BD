from sqlalchemy import Column, Integer, ForeignKey, String, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Transformacion(Base):
    __tablename__ = "transformaciones"
    
    id_transformacion = Column(Integer, primary_key=True, autoincrement=True)
    id_imagen = Column(Integer, ForeignKey("imagenes.id_imagen"), nullable=False)
    tipo = Column(String(50), nullable=False)
    parametros = Column(JSON, nullable=True)
    orden = Column(Integer, default=0)
    
    imagen = relationship("Imagen", back_populates="transformaciones")