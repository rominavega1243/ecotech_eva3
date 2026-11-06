from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from servicios.permisos import exigir_sesion

def obtener_mis_registros(sesion):
    exigir_sesion(sesion)
    
    empleado_id = None

    if isinstance(sesion, dict):
        empleado_id = sesion.get("empleado_id") or sesion.get("empleado")
    else:
        empleado_id = getattr(sesion, "empleado_id", None)
        if empleado_id is None and hasattr(sesion, "empleado"):
            emp_val = getattr(sesion, "empleado")
            empleado_id = getattr(emp_val, "id", emp_val)

    if empleado_id is None:
        return []

    return RegistroTiempoDAO.buscar_por_empleado_id(int(empleado_id))