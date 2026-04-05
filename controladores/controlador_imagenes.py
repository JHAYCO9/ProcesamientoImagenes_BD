from modelos import Imagen, EstadoImagen
from gestor import IGestorBD

class ControladorImagenes:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd
    
    def crear_imagen(self, datos: dict) -> dict:
        img = Imagen(
            id_lote=datos.get('id_lote'),
            nombre_archivo=datos.get('nombre_archivo'),
            ruta_original=datos.get('ruta_original'),
            formato_original=datos.get('formato_original'),
            tamano_bytes=datos.get('tamano_bytes', 0)
        )
        img = self.gestor_bd.guardar_imagen(img)
        return {"id_imagen": img.id_imagen, "estado": img.estado.value}
    
    def obtener_imagen(self, id: int) -> dict:
        imagenes = self.gestor_bd.obtener(Imagen, {"id_imagen": id})
        if imagenes:
            i = imagenes[0]
            return {
                "id_imagen": i.id_imagen,
                "nombre_archivo": i.nombre_archivo,
                "estado": i.estado.value,
                "formato_original": i.formato_original,
                "formato_resultado": i.formato_resultado
            }
        return None
    
    def actualizar_imagen(self, id: int, datos: dict) -> dict:
        # Actualizar la imagen
        img = self.gestor_bd.actualizar(Imagen, id, datos)
        if img:
            # Si la imagen se completa, actualizar el lote
            if datos.get('estado') == EstadoImagen.LISTO:
                lote = self.gestor_bd.obtener(SolicitudLote, {"id_lote": img.id_lote})[0]
                nuevas_completadas = lote.imagenes_completadas + 1
                self.gestor_bd.actualizar(SolicitudLote, lote.id_lote, 
                                         {"imagenes_completadas": nuevas_completadas})
                
                if lote.esta_completo():
                    self.gestor_bd.actualizar_estado_lote(lote.id_lote, EstadoLote.COMPLETADO)
            
            return {"id_imagen": img.id_imagen, "estado": img.estado.value}
        return None
    
    def obtener_por_lote(self, id_lote: int) -> list:
        imagenes = self.gestor_bd.obtener(Imagen, {"id_lote": id_lote})
        return [{"id_imagen": i.id_imagen, "nombre_archivo": i.nombre_archivo, "estado": i.estado.value} for i in imagenes]