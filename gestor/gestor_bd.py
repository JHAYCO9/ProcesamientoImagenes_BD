from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from typing import List, Dict, Optional
from modelos import Base, Usuario, SolicitudLote, Imagen, Transformacion, Nodo, LogEjecucion, EstadoLote, EstadoImagen, EstadoNodo

class IGestorBD:
    def guardar(self, entidad): pass
    def obtener(self, modelo, filtros): pass
    def actualizar(self, modelo, id, datos): pass
    def eliminar(self, modelo, id): pass

class GestorBD(IGestorBD):
    def __init__(self, url_bd: str):
        self.url_bd = url_bd
        
        # Configurar SSL para MySQL si es necesario
        connect_args = {}
        if 'mysql' in url_bd:
            # Para MySQL con Aiven
            import ssl
            connect_args = {
                'ssl': {
                    'ca': 'ca.pem'  # El archivo ca.pem debe estar en la raíz
                }
            }
        
        self.engine = create_engine(
            url_bd, 
            echo=False, 
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args=connect_args if connect_args else None
        )
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
    
    def crear_tablas(self):
        """Crea todas las tablas en la base de datos"""
        Base.metadata.create_all(self.engine)
    
    def guardar(self, entidad):
        session = self.Session()
        try:
            session.add(entidad)
            session.commit()
            session.refresh(entidad)
            return entidad
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def obtener(self, modelo, filtros: Dict = None):
        session = self.Session()
        try:
            query = session.query(modelo)
            if filtros:
                query = query.filter_by(**filtros)
            return query.all()
        finally:
            session.close()
    
    def obtener_uno(self, modelo, filtros: Dict = None):
        session = self.Session()
        try:
            query = session.query(modelo)
            if filtros:
                query = query.filter_by(**filtros)
            return query.first()
        finally:
            session.close()
    
    def actualizar(self, modelo, id: int, datos: Dict):
        session = self.Session()
        try:
            # Usar filter_by en lugar de session.get para evitar problemas de caché con MySQL
            pk_col = modelo.__mapper__.primary_key[0].name
            entidad = session.query(modelo).filter(
                modelo.__mapper__.primary_key[0] == id
            ).first()
            print(f"[DEBUG actualizar] modelo={modelo.__tablename__} id={id} encontrado={entidad is not None}")
            if entidad:
                for key, value in datos.items():
                    if hasattr(entidad, key):
                        setattr(entidad, key, value)
                session.commit()
                session.refresh(entidad)
                return entidad
            return None
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def eliminar(self, modelo, id: int):
        session = self.Session()
        try:
            entidad = session.get(modelo, id)   # ← cambiar esta línea
            if entidad:
                session.delete(entidad)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    # Métodos específicos del diagrama
    def guardar_usuario(self, u):
        return self.guardar(u)
    
    def obtener_usuario_por_email(self, email):
        return self.obtener_uno(Usuario, {"email": email})
    
    def guardar_solicitud_lote(self, s):
        return self.guardar(s)
    
    def actualizar_estado_lote(self, id, estado):
        return self.actualizar(SolicitudLote, id, {"estado": estado})
    
    def guardar_imagen(self, img):
        return self.guardar(img)
    
    def actualizar_imagen(self, img):
        return self.guardar(img)
    
    def guardar_transformacion(self, t):
        return self.guardar(t)
    
    def actualizar_transformacion(self, t):
        return self.guardar(t)
    
    def guardar_nodo(self, n):
        return self.guardar(n)
    
    def actualizar_nodo(self, id, estado):
        return self.actualizar(Nodo, id, {"estado": estado})
    
    def obtener_nodos_activos(self):
        return self.obtener(Nodo, {"estado": EstadoNodo.ACTIVO})
    
    def guardar_log(self, log):
        return self.guardar(log)
    
    def obtener_logs_por_imagen(self, id_imagen):
        return self.obtener(LogEjecucion, {"id_imagen": id_imagen})
    
    def obtener_historial_usuario(self, id_usuario):
        return self.obtener(SolicitudLote, {"id_usuario": id_usuario})
    
    def probar_conexion(self):
        """Prueba la conexión a la base de datos"""
        try:
            session = self.Session()
            # Usar text() para SQL puro
            session.execute(text("SELECT 1"))
            session.close()
            print("Conexión a la base de datos exitosa")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False    
    def incrementar_completadas_atomico(self, id_lote: int) -> object:
        """
        Incrementa imagenes_completadas en 1 de forma atómica usando SQL directo,
        evitando condiciones de carrera cuando múltiples nodos terminan a la vez.
        Retorna el lote actualizado.
        """
        session = self.Session()
        try:
            session.execute(
                text(
                    "UPDATE solicitudes_lote "
                    "SET imagenes_completadas = imagenes_completadas + 1 "
                    "WHERE id_lote = :id"
                ),
                {"id": id_lote}
            )
            session.commit()
            # Releer el lote para ver el valor real tras el commit
            lote = session.query(SolicitudLote).filter(
                SolicitudLote.id_lote == id_lote
            ).first()
            if lote and lote.total_imagenes > 0:
                if lote.imagenes_completadas >= lote.total_imagenes:
                    lote.estado = EstadoLote.COMPLETADO
                elif lote.estado == EstadoLote.PENDIENTE:
                    lote.estado = EstadoLote.EN_PROCESO
                session.commit()
                session.refresh(lote)
            return lote
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()