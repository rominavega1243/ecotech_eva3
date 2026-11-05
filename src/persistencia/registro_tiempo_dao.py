from persistencia.crear_bd import abrir_conexion
from dominio.registro_tiempo import RegistroTiempo

class RegistroTiempoDAO:

    @classmethod
    def insertar(cls, registro):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        
        # Extraer el ID del empleado sin importar cómo se llame en la clase RegistroTiempo
        emp_id = getattr(registro, 'empleado_id', None)
        if emp_id is None:
            emp_id = getattr(registro, 'id_empleado', None)
        if emp_id is None and hasattr(registro, 'empleado'):
            emp = getattr(registro, 'empleado')
            emp_id = getattr(emp, 'id', emp)

        # Extraer el ID del proyecto
        proy_id = getattr(registro, 'proyecto_id', None)
        if proy_id is None:
            proy_id = getattr(registro, 'id_proyecto', None)

        sql = """
            INSERT INTO registro_tiempo (fecha, cantidad_horas, tareas_realizadas, empleado_id, proyecto_id)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (
            registro.fecha,
            registro.cantidad_horas,
            registro.tareas_realizadas,
            emp_id,
            proy_id
        ))
        conexion.commit()
        conexion.close()

    @classmethod
    def obtener_todos(cls):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo")
        filas = cursor.fetchall()
        conexion.close()
        
        registros = []
        for f in filas:
            reg = RegistroTiempo(f[1], f[2], f[3], f[4], f[5], f[6])
            reg.id = f[0]
            registros.append(reg)
        return registros

    @classmethod
    def buscar_por_empleado_id(cls, empleado_id):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        # Buscamos asegurando el filtro por empleado_id exacto
        sql = "SELECT id, fecha, cantidad_horas, tareas_realizadas, descripcion, empleado_id, proyecto_id FROM registro_tiempo WHERE empleado_id = ?"
        cursor.execute(sql, (int(empleado_id),))
        filas = cursor.fetchall()
        conexion.close()

        registros = []
        for f in filas:
            reg = RegistroTiempo(f[1], f[2], f[3], f[4], f[5], f[6])
            reg.id = f[0]
            registros.append(reg)
        return registros