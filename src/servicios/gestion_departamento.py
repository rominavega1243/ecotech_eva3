from persistencia.departamento_dao import DepartamentoDAO

def listar_departamentos():
    """Consulta la BD y retorna la lista de departamentos."""
    dao = DepartamentoDAO()
    return dao.obtener_todos()

def crear_departamento(nombre):
    """Inserta un nuevo departamento en la BD."""
    dao = DepartamentoDAO()
    return dao.insertar(nombre)

def actualizar_departamento(dep_id, nuevo_nombre):
    """Actualiza un departamento en la BD."""
    dao = DepartamentoDAO()
    return dao.actualizar(dep_id, nuevo_nombre)

def eliminar_departamento(dep_id):
    """Elimina un departamento de la BD."""
    dao = DepartamentoDAO()
    return dao.eliminar(dep_id)