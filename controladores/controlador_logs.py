from modelos import LogEjecucion, NivelLog
from gestor import IGestorBD

class ControladorLogs:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd
    
    def guardar_log(self, datos: dict) -> dict:
        nivel_str = datos.get('nivel', 'INFO').upper()  # ← forzar mayúsculas
        log = LogEjecucion(
            id_imagen=datos.get('id_imagen'),
            id_nodo=datos.get('id_nodo'),
            mensaje=datos.get('mensaje'),
            nivel=NivelLog(nivel_str)
        )
        log = self.gestor_bd.guardar_log(log)
        return {"id_log": log.id_log, "timestamp": log.timestamp.isoformat()}
    
    def obtener_logs_imagen(self, id_imagen: int) -> list:
        logs = self.gestor_bd.obtener_logs_por_imagen(id_imagen)
        return [{"id_log": l.id_log, "mensaje": l.mensaje, "nivel": l.nivel.value, 
                 "timestamp": l.timestamp.isoformat()} for l in logs]
    
    def obtener_logs_nodo(self, id_nodo: int) -> list:
        logs = self.gestor_bd.obtener(LogEjecucion, {"id_nodo": id_nodo})
        return [{"id_log": l.id_log, "mensaje": l.mensaje, "nivel": l.nivel.value,
                 "timestamp": l.timestamp.isoformat()} for l in logs]