from modelos import Nodo, EstadoNodo
from gestor import IGestorBD


class ControladorNodos:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd

    def registrar_nodo(self, datos: dict) -> dict:
        identificador = datos.get("identificador") or datos.get("nombre")
        direccion_red = datos.get("direccion_red") or datos.get("direccion_ip", "localhost")
        puerto_pyro5  = datos.get("puerto_pyro5")  or datos.get("puerto", 9090)

        # Buscar si el nodo ya existe por identificador
        existentes = self.gestor_bd.obtener(Nodo, {"identificador": identificador})

        if existentes:
            # Ya existe → actualizarlo (marcar como ACTIVO y actualizar dirección/puerto)
            n = existentes[0]
            n = self.gestor_bd.actualizar(Nodo, n.id_nodo, {
                "estado":        EstadoNodo.ACTIVO,
                "direccion_red": direccion_red,
                "puerto_pyro5":  puerto_pyro5,
            })
        else:
            # No existe → crearlo
            n = Nodo(
                identificador = identificador,
                direccion_red = direccion_red,
                puerto_pyro5  = puerto_pyro5,
                estado        = EstadoNodo.ACTIVO,
            )
            n = self.gestor_bd.guardar_nodo(n)

        return {
            "id_nodo":       n.id_nodo,
            "identificador": n.identificador,
            "estado":        n.estado.value
        }

    def actualizar_estado(self, id: int, estado: str) -> dict:
        estado_upper = estado.upper()
        estado_enum  = EstadoNodo(estado_upper)
        n = self.gestor_bd.actualizar_nodo(id, estado_enum)
        if n:
            return {"id_nodo": n.id_nodo, "estado": n.estado.value}
        return None

    def obtener_nodos_activos(self) -> list:
        nodos = self.gestor_bd.obtener_nodos_activos()
        return [
            {
                "id_nodo":       n.id_nodo,
                "identificador": n.identificador,
                "direccion":     f"{n.direccion_red}:{n.puerto_pyro5}",
                "estado":        n.estado.value,
            }
            for n in nodos
        ]

    def listar_todos(self) -> list:
        """Lista todos los nodos registrados con su estado actual (ACTIVO/INACTIVO/ERROR)."""
        nodos = self.gestor_bd.obtener(Nodo, {})
        return [
            {
                "id_nodo":         n.id_nodo,
                "identificador":   n.identificador,
                "direccion_red":   n.direccion_red,
                "puerto_pyro5":    n.puerto_pyro5,
                "estado":          n.estado.value,
                "trabajos_activos": n.trabajos_activos,
            }
            for n in nodos
        ]

    def obtener_nodo(self, id: int) -> dict:
        nodos = self.gestor_bd.obtener(Nodo, {"id_nodo": id})
        if nodos:
            n = nodos[0]
            return {
                "id_nodo":         n.id_nodo,
                "identificador":   n.identificador,
                "direccion_red":   n.direccion_red,
                "puerto_pyro5":    n.puerto_pyro5,
                "estado":          n.estado.value,
                "trabajos_activos": n.trabajos_activos
            }
        return None