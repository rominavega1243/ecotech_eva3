from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from dominio.empleado import Empleado
from dominio.departamento import Departamento
from dominio.proyecto import Proyecto
from dominio.registro_tiempo import RegistroTiempo
from dominio.usuario import Usuario
from servicios.autenticacion import crear_hash
from persistencia.crear_bd import abrir_conexion

def cargar_semillas():
    conexion = abrir_conexion()
    print("Iniciando carga de semillas...")

    # 1. Departamentos
    datos_deptos = [
        ("Tecnología", "Carlos Mendoza"),
        ("Recursos Humanos", "Laura Gómez"),
        ("Finanzas", "Roberto Dávila"),
        ("Marketing", "Sofía Castro"),
        ("Operaciones", "Javier Silva")
    ]
    departamentos_db = []
    for nombre, gerente in datos_deptos:
        depto = DepartamentoDAO.buscar_por_nombre(nombre)
        if not depto:
            depto = Departamento(idDepartamento=None, nombre=nombre, gerente=gerente)
            DepartamentoDAO.insertar(depto)
            depto = DepartamentoDAO.buscar_por_nombre(nombre)
        departamentos_db.append(depto)
    print(" Departamentos cargados.")

    # 2. Empleados
    datos_empleados = [
        ("Ana Torres", "ana@ecotech.example", "555-0101", "2023-01-15", 3500),
        ("Luis Vargas", "luis@ecotech.example", "555-0102", "2023-02-01", 3200),
        ("María Rojas", "maria@ecotech.example", "555-0103", "2022-11-20", 3800),
        ("Pedro Soto", "pedro@ecotech.example", "555-0104", "2023-03-10", 3100),
        ("Elena Díaz", "elena@ecotech.example", "555-0105", "2021-08-05", 4200),
        ("Diego Vega", "diego@ecotech.example", "555-0106", "2022-05-12", 3400),
        ("Carmen Luna", "carmen@ecotech.example", "555-0107", "2023-06-22", 3300),
        ("Raúl Mora", "raul@ecotech.example", "555-0108", "2021-12-01", 4500),
        ("Sara Peña", "sara@ecotech.example", "555-0109", "2023-07-15", 3000),
        ("Hugo Ríos", "hugo@ecotech.example", "555-0110", "2020-03-30", 4800),
        ("Irene Paz", "irene@ecotech.example", "555-0111", "2022-09-18", 3600),
        ("Jorge Gil", "jorge@ecotech.example", "555-0112", "2023-01-05", 3100),
        ("Lucía Sol", "lucia@ecotech.example", "555-0113", "2021-04-14", 4100),
        ("Mario Rey", "mario@ecotech.example", "555-0114", "2023-08-01", 2900),
        ("Nuria Cid", "nuria@ecotech.example", "555-0115", "2022-10-10", 3700),
        ("Óscar Pou", "oscar@ecotech.example", "555-0116", "2021-07-25", 4300),
        ("Paula Cruz", "paula@ecotech.example", "555-0117", "2023-05-08", 3200),
        ("René Alba", "rene@ecotech.example", "555-0118", "2020-11-11", 4600),
        ("Teresa Mas", "teresa@ecotech.example", "555-0119", "2022-02-28", 3900),
        ("Víctor Roa", "victor@ecotech.example", "555-0120", "2023-09-15", 3000)
    ]
    empleados_db = []
    for nombre, correo, telefono, fecha, salario in datos_empleados:
        empleado = EmpleadoDAO.buscar_por_correo(correo)
        if not empleado:
            empleado = Empleado(nombre, correo, telefono, fecha, salario)
            EmpleadoDAO.insertar(empleado)
            empleado = EmpleadoDAO.buscar_por_correo(correo)
        empleados_db.append(empleado)
    print(" Empleados cargados correctamente.")

    # 3. Proyectos
    datos_proyectos = [
        ("Migración a la Nube", "Migración de servidores locales a AWS", "2025-03-05"),
        ("Campaña publicitaria", "Lanzamiento del producto estrella", "2025-02-15"),
        ("Auditoría Interna", "Revisión anual de procesos financieros", "2026-03-15")
    ]
    proyectos_db = []
    for nombre, desc, fecha in datos_proyectos:
        proyecto = ProyectoDAO.buscar_por_nombre(nombre)
        if not proyecto:
            proyecto = Proyecto(nombre, desc, fecha)
            ProyectoDAO.insertar(proyecto)
            proyecto = ProyectoDAO.buscar_por_nombre(nombre)
        proyectos_db.append(proyecto)
    print(" Proyectos cargados correctamente.")

    # 4. Registros de tiempo
    if empleados_db and proyectos_db:
        try:
            registros_existentes = RegistroTiempoDAO.obtener_todos()
        except AttributeError:
            registros_existentes = []

        if not registros_existentes: 
            registros = [
                ("2024-04-01", 4.5, "Configuración de servidores", "Setup inicial", empleados_db[0].id, proyectos_db[0].id),
                ("2024-04-02", 3.0, "Migración de base de datos", "Scripts de SQL", empleados_db[1].id, proyectos_db[0].id),
                ("2024-04-03", 5.0, "Reunión de planificación", "Definición de KPIs", empleados_db[12].id, proyectos_db[1].id)
            ]
            for fecha, horas, tareas, desc, emp_id, proy_id in registros:
                registro = RegistroTiempo(fecha, horas, tareas, emp_id, proy_id)
                RegistroTiempoDAO.insertar(registro)
            print(" Registros de tiempo cargados correctamente.")
        else:
            print(" Los registros de tiempo ya existían. Se omitió la inserción.")

    # 5. Usuario Administrador Inicial
    if empleados_db:
        usuario_admin = UsuarioDAO.buscar_por_nombre_usuario("admin")
        if not usuario_admin:
            hash_clave = crear_hash("admin123")
            nuevo_usuario = Usuario("admin", hash_clave, empleado_id=empleados_db[0].id)
            UsuarioDAO.insertar(nuevo_usuario)
            print(" Usuario inicial (admin) cargado con clave cifrada.")
        else:
            print(" El usuario inicial ya existía.")

    print(" Base de datos poblada exitosamente.")
    conexion.commit()
    conexion.close()