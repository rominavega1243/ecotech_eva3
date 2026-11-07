from persistencia.conexion import abrir_conexion, marcador_sql
from dominio.proyecto import Proyecto

class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marcador = marcador_sql()
            sql = f"""
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                VALUES ({marcador}, {marcador}, {marcador})
            """
            cursor.execute(sql, (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio))
            proyecto.id = cursor.lastrowid
            conexion.commit()
            return proyecto
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre):
        conn = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            marcador = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre, descripcion, fecha_inicio FROM proyecto WHERE nombre = {marcador}",
                (nombre,)
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            proyecto = Proyecto(nombre=fila[1], descripcion=fila[2], fecha_inicio=fila[3])
            proyecto.id = fila[0]
            return proyecto
        finally:
            if conn:
                conn.close()

    @staticmethod
    def listar_proyectos():
        conn = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, descripcion, fecha_inicio FROM proyecto")
            proyectos = cursor.fetchall()
            return proyectos
        finally:
            if conn:
                conn.close()

    @staticmethod
    def buscar_por_id(id_proyecto):
        conn = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            marcador = marcador_sql()
            cursor.execute(
                f"SELECT id, nombre, descripcion, fecha_inicio FROM proyecto WHERE id = {marcador}",
                (id_proyecto,)
            )
            fila = cursor.fetchone()
            if fila is None:
                return None
            # SOLUCIÓN DEL ERROR 'tuple object has no attribute nombre'
            # Convertimos la tupla en un objeto Proyecto antes de retornarlo
            proyecto = Proyecto(nombre=fila[1], descripcion=fila[2], fecha_inicio=fila[3])
            proyecto.id = fila[0]
            return proyecto
        finally:
            if conn:
                conn.close()

    # Le cambié el nombre a 'actualizar' para que calce perfecto con tu menú
    @staticmethod
    def actualizar(proyecto):
        conn = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            marcador = marcador_sql()
            cursor.execute(
                f"UPDATE proyecto SET nombre = {marcador}, descripcion = {marcador}, fecha_inicio = {marcador} WHERE id = {marcador}",
                (proyecto.nombre, proyecto.descripcion, proyecto.fecha_inicio, proyecto.id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if conn:
                conn.close()

    # Le cambié el nombre a 'eliminar' para que calce perfecto con tu menú
    @staticmethod
    def eliminar(id_proyecto):
        conn = None
        try:
            conn = abrir_conexion()
            cursor = conn.cursor()
            marcador = marcador_sql()
            cursor.execute(f"DELETE FROM proyecto WHERE id = {marcador}", (id_proyecto,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            if conn:
                conn.close()