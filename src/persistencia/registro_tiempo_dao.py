from persistencia.crear_bd import abrir_conexion
from dominio.registro_tiempo import RegistroTiempo

class RegistroTiempoDAO:

    @classmethod
    def insertar(cls, registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            
            emp_id = getattr(registro, 'empleado_id', None)
            proy_id = getattr(registro, 'proyecto_id', None)

            sql = """
                INSERT INTO registro_tiempo (fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (
                registro.fecha,
                registro.cantidad_horas,
                registro.tareas_realizadas,
                registro.descripcion,
                emp_id,
                proy_id
            ))
            conexion.commit()
            return True
        finally:
            if conexion:
                conexion.close()

    @classmethod
    def obtener_todos(cls):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo")
            filas = cursor.fetchall()
            
            registros = []
            for f in filas:
                reg = RegistroTiempo(
                    fecha=f[1],
                    cantidad_horas=f[2],
                    tareas_realizadas=f[3],
                    descripcion=f[4],
                    empleado_id=f[5],
                    proyecto_id=f[6],
                    id=f[0]
                )
                registros.append(reg)
            return registros
        finally:
            if conexion:
                conexion.close()

    @classmethod
    def buscar_por_empleado_id(cls, empleado_id):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            sql = "SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo WHERE empleado_id = ?"
            cursor.execute(sql, (int(empleado_id),))
            filas = cursor.fetchall()

            registros = []
            for f in filas:
                reg = RegistroTiempo(
                    fecha=f[1],
                    cantidad_horas=f[2],
                    tareas_realizadas=f[3],
                    descripcion=f[4],
                    empleado_id=f[5],
                    proyecto_id=f[6],
                    id=f[0]
                )
                registros.append(reg)
            return registros
        finally:
            if conexion:
                conexion.close()

    # --- NUEVOS MÉTODOS AÑADIDOS PARA COMPLETAR EL CRUD ---

    @classmethod
    def buscar_por_id(cls, id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            sql = "SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo WHERE id = ?"
            cursor.execute(sql, (id_registro,))
            f = cursor.fetchone()
            
            if f is None:
                return None
                
            return RegistroTiempo(
                fecha=f[1],
                cantidad_horas=f[2],
                tareas_realizadas=f[3],
                descripcion=f[4],
                empleado_id=f[5],
                proyecto_id=f[6],
                id=f[0]
            )
        finally:
            if conexion:
                conexion.close()

    @classmethod
    def actualizar(cls, registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            
            emp_id = getattr(registro, 'empleado_id', None)
            proy_id = getattr(registro, 'proyecto_id', None)

            sql = """
                UPDATE registro_tiempo 
                SET fecha = ?, cantidad_horas = ?, tareas_realizadas = ?, descripcion = ?, empleado_id = ?, proyecto_id = ?
                WHERE id = ?
            """
            cursor.execute(sql, (
                registro.fecha,
                registro.cantidad_horas,
                registro.tareas_realizadas,
                registro.descripcion,
                emp_id,
                proy_id,
                registro.id
            ))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            if conexion:
                conexion.close()

    @classmethod
    def eliminar(cls, id_registro):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            sql = "DELETE FROM registro_tiempo WHERE id = ?"
            cursor.execute(sql, (id_registro,))
            conexion.commit()
            return cursor.rowcount > 0
        finally:
            if conexion:
                conexion.close()