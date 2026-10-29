from dominio.empleado import Empleado

class Departamento:
    def __init__(self, idDepartamento: int , nombre: str , gerente: str):
        self.idDepartamento = idDepartamento
        self.nombre = nombre
        self.gerente = gerente
        self._empleados: list[Empleado] = []


    def agregar_empleado(self, empleado: Empleado) -> bool:
        if empleado in self._empleados:
            return False