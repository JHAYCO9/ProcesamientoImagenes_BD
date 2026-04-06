from modelos import Imagen, EstadoImagen, SolicitudLote, EstadoLote, Transformacion, TipoTransformacion, EstadoTransformacion
from gestor import IGestorBD


class ControladorImagenes:
    def __init__(self, gestor_bd: IGestorBD):
        self.gestor_bd = gestor_bd

    def crear_imagen(self, datos: dict) -> dict:
        nombre    = datos.get('nombre_archivo', '')
        extension = nombre.rsplit('.', 1)[-1].upper() if '.' in nombre else 'PNG'

        img = Imagen(
            id_lote          = datos.get('id_lote'),
            nombre_archivo   = nombre,
            ruta_original    = datos.get('ruta_original', f'temp/{nombre}'),
            formato_original = datos.get('formato_original', extension),
            tamano_bytes     = datos.get('tamano_bytes', 0),
            estado           = EstadoImagen.PENDIENTE
        )
        img = self.gestor_bd.guardar_imagen(img)
        return {"id_imagen": img.id_imagen, "estado": img.estado.value}

    def obtener_imagen(self, id: int) -> dict:
        imagenes = self.gestor_bd.obtener(Imagen, {"id_imagen": id})
        if imagenes:
            i = imagenes[0]
            return {
                "id_imagen":         i.id_imagen,
                "id_lote":           i.id_lote,
                "id_nodo":           i.id_nodo,
                "nombre_archivo":    i.nombre_archivo,
                "estado":            i.estado.value,
                "formato_original":  i.formato_original,
                "formato_resultado": i.formato_resultado,
                "ruta_resultado":    i.ruta_resultado,
                "fecha_recepcion":   i.fecha_recepcion.isoformat() if i.fecha_recepcion else None,
                "fecha_conversion":  i.fecha_conversion.isoformat() if i.fecha_conversion else None,
            }
        return None

    def actualizar_imagen(self, id: int, datos: dict) -> dict:
        # Convertir estado string a enum si viene como string
        if 'estado' in datos and isinstance(datos['estado'], str):
            datos['estado'] = EstadoImagen(datos['estado'])

        # Si llega a estado LISTO o ERROR, registrar fecha_conversion
        if datos.get('estado') in (EstadoImagen.LISTO, EstadoImagen.ERROR):
            from datetime import datetime
            datos.setdefault('fecha_conversion', datetime.utcnow())

        img = self.gestor_bd.actualizar(Imagen, id, datos)
        if img:
            return {"id_imagen": img.id_imagen, "estado": img.estado.value}
        return None

    def obtener_por_lote(self, id_lote: int) -> list:
        imagenes = self.gestor_bd.obtener(Imagen, {"id_lote": id_lote})
        return [
            {
                "id_imagen":      i.id_imagen,
                "nombre_archivo": i.nombre_archivo,
                "estado":         i.estado.value,
                "ruta_resultado": i.ruta_resultado,
                "id_nodo":        i.id_nodo,
            }
            for i in imagenes
        ]

    def crear_transformacion(self, datos: dict) -> dict:
        t = Transformacion(
            id_imagen  = datos.get('id_imagen'),
            tipo       = TipoTransformacion(datos.get('tipo')),
            parametros = datos.get('parametros', {}),
            orden      = datos.get('orden', 0),
            estado     = EstadoTransformacion(datos.get('estado', 'PENDIENTE'))
        )
        t = self.gestor_bd.guardar_transformacion(t)
        return {"id_transformacion": t.id_transformacion, "estado": t.estado.value}

    def actualizar_transformacion(self, id: int, datos: dict) -> dict:
        if 'estado' in datos and isinstance(datos['estado'], str):
            datos['estado'] = EstadoTransformacion(datos['estado'])
        t = self.gestor_bd.actualizar(Transformacion, id, datos)
        return {"id_transformacion": t.id_transformacion, "estado": t.estado.value} if t else None

    def obtener_transformaciones(self, id_imagen: int) -> list:
        """Retorna todas las transformaciones registradas para una imagen."""
        transformaciones = self.gestor_bd.obtener(Transformacion, {"id_imagen": id_imagen})
        return [
            {
                "id_transformacion": t.id_transformacion,
                "tipo":              t.tipo.value,
                "parametros":        t.parametros,
                "orden":             t.orden,
                "estado":            t.estado.value,
            }
            for t in transformaciones
        ]