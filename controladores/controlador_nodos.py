from modelos import Nodo, EstadoNodo
from gestor import IGestorBD

class ControladorNodos:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd
    
    def registrar_nodo(self, datos: dict) -> dict:
        n = Nodo(
            nombre=datos.get('nombre'),
            direccion_ip=datos.get('direccion_ip'),
            puerto=datos.get('puerto', 5000),
            capacidad_maxima=datos.get('capacidad_maxima', 10)
        )
        n = self.gestor_bd.guardar_nodo(n)
        return {"id_nodo": n.id_nodo, "nombre": n.nombre, "estado": n.estado.value}
    
    def actualizar_estado(self, id: int, estado: str) -> dict:
        estado_enum = EstadoNodo(estado)
        n = self.gestor_bd.actualizar_nodo(id, estado_enum)
        if n:
            return {"id_nodo": n.id_nodo, "estado": n.estado.value}
        return None
    
    def obtener_nodos_activos(self) -> list:
        nodos = self.gestor_bd.obtener_nodos_activos()
        return [{"id_nodo": n.id_nodo, "nombre": n.nombre, "direccion": f"{n.direccion_ip}:{n.puerto}"} for n in nodos]
    
    def obtener_nodo(self, id: int) -> dict:
        nodos = self.gestor_bd.obtener(Nodo, {"id_nodo": id})
        if nodos:
            n = nodos[0]
            return {"id_nodo": n.id_nodo, "nombre": n.nombre, "direccion_ip": n.direccion_ip, 
                    "puerto": n.puerto, "estado": n.estado.value, "carga_actual": n.carga_actual}
        return None