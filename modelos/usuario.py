from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class RolUsuario(enum.Enum):
    ADMIN = "admin"
    USUARIO = "usuario"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    rol = Column(Enum(RolUsuario), default=RolUsuario.USUARIO)
    
    solicitudes = relationship("SolicitudLote", back_populates="usuario")
    
    def set_password(self, raw_password: str):
        import hashlib
        self.password_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    
    def verificar_password(self, raw_password: str) -> bool:
        import hashlib
        return self.password_hash == hashlib.sha256(raw_password.encode()).hexdigest()
    
    def get_solicitudes(self):
        return self.solicitudes