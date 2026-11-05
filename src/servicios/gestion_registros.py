from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion

def obtener_mis_registros(sesion):
    exigir_sesion(sesion)
    
    empleado_id = None

    # 1. Si sesion es un diccionario
    if isinstance(sesion, dict):
        empleado_id = sesion.get("empleado_id") or sesion.get("empleado")
    else:
        # 2. Intentar extraer empleado_id directamente
        empleado_id = getattr(sesion, "empleado_id", None)
        
        # 3. Si no existe, extraer de la propiedad 'empleado' (que tiene el valor 2 que imprime Mi ficha)
        if empleado_id is None and hasattr(sesion, "empleado"):
            emp_val = getattr(sesion, "empleado")
            # Si 'empleado' es un objeto con id (emp_val.id) o si ya es el entero 
            empleado_id = getattr(emp_val, "id", emp_val)

    if empleado_id is None:
        return []

    # 4. Consultar al DAO forzando la conversión a número entero 
    return RegistroTiempoDAO.buscar_por_empleado_id(int(empleado_id))