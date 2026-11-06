from persistencia.proyecto_dao import ProyectoDAO

def listar_proyectos():
    """Consulta la BD y retorna la lista de proyectos."""
    dao = ProyectoDAO()
    return dao.obtener_todos()

def crear_proyecto(nombre):
    """Inserta un nuevo proyecto en la BD."""
    dao = ProyectoDAO()
    return dao.insertar(nombre)

def actualizar_proyecto(proy_id, nuevo_nombre):
    """Actualiza un proyecto en la BD."""
    dao = ProyectoDAO()
    return dao.actualizar(proy_id, nuevo_nombre)

def eliminar_proyecto(proy_id):
    """Elimina un proyecto de la BD."""
    dao = ProyectoDAO()
    return dao.eliminar(proy_id)