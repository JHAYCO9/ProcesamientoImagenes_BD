from modelos import SolicitudLote, EstadoLote
from gestor import IGestorBD


class ControladorLotes:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd

    def crear_lote(self, datos: dict) -> dict:
        l = SolicitudLote(
            id_usuario     = datos.get('id_usuario'),
            total_imagenes = datos.get('total_imagenes', 0)
        )
        l = self.gestor_bd.guardar_solicitud_lote(l)
        return {"id_lote": l.id_lote, "estado": l.estado.value}

    def obtener_lote(self, id: int) -> dict:
        lotes = self.gestor_bd.obtener(SolicitudLote, {"id_lote": id})
        if lotes:
            l = lotes[0]
            return {
                "id_lote":              l.id_lote,
                "id_usuario":           l.id_usuario,
                "estado":               l.estado.value,
                "progreso":             l.get_progreso(),
                "total_imagenes":       l.total_imagenes,
                "imagenes_completadas": l.imagenes_completadas
            }
        return None

    def actualizar_estado(self, id: int, estado: str) -> dict:
        estado_enum = EstadoLote(estado)
        l = self.gestor_bd.actualizar_estado_lote(id, estado_enum)
        if l:
            return {"id_lote": l.id_lote, "estado": l.estado.value}
        return None

    def incrementar_completadas(self, id_lote: int) -> dict:
        """
        Incrementa imagenes_completadas de forma ATÓMICA (SQL directo)
        para evitar condiciones de carrera cuando varios nodos terminan a la vez.
        Actualiza automáticamente el estado del lote a EN_PROCESO o COMPLETADO.
        """
        l = self.gestor_bd.incrementar_completadas_atomico(id_lote)
        if l:
            return {
                "id_lote":              l.id_lote,
                "estado":               l.estado.value,
                "imagenes_completadas": l.imagenes_completadas,
                "total_imagenes":       l.total_imagenes,
                "progreso":             l.get_progreso()
            }
        return None

    def obtener_historial(self, id_usuario: int) -> list:
        lotes = self.gestor_bd.obtener_historial_usuario(id_usuario)
        return [
            {
                "id_lote":              l.id_lote,
                "estado":               l.estado.value,
                "progreso":             l.get_progreso(),
                "total_imagenes":       l.total_imagenes,
                "imagenes_completadas": l.imagenes_completadas
            }
            for l in lotes
        ]