from modelos import Usuario
from gestor import IGestorBD

class ControladorUsuarios:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd
    
    def crear_usuario(self, datos: dict) -> dict:
        u = Usuario(
            nombre=datos.get('nombre'),
            email=datos.get('email')
        )
        u.set_password(datos.get('password'))
        u = self.gestor_bd.guardar_usuario(u)
        return {"id_usuario": u.id_usuario, "nombre": u.nombre, "email": u.email}
    
    def obtener_usuario(self, id: int) -> dict:
        usuarios = self.gestor_bd.obtener(Usuario, {"id_usuario": id})
        if usuarios:
            u = usuarios[0]
            return {"id_usuario": u.id_usuario, "nombre": u.nombre, "email": u.email, "activo": u.activo}
        return None
    
    def obtener_por_email(self, email: str) -> dict:
        u = self.gestor_bd.obtener_usuario_por_email(email)
        if u:
            return {"id_usuario": u.id_usuario, "nombre": u.nombre, "email": u.email}
        return None
    
    def actualizar_usuario(self, id: int, datos: dict) -> dict:
        u = self.gestor_bd.actualizar(Usuario, id, datos)
        if u:
            return {"id_usuario": u.id_usuario, "nombre": u.nombre, "email": u.email}
        return None
    
    def eliminar_usuario(self, id: int):
        self.gestor_bd.eliminar(Usuario, id)