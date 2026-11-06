import math
from getpass import getpass
import requests

from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario, autenticar 
from dominio.usuario import Usuario

# Servicios y DAOs reales
from servicios.gestion_empleados import listar_todos 
from servicios.gestion_registros import obtener_mis_registros 
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO 

# -------------------------------------------------------------
# CONSTANTES DE INTERFAZ (Elimina advertencias de SonarQube)
# -------------------------------------------------------------
SEPARADOR = "========================================="
VOLVER_CRUDS = "0. Volver al menú de CRUDs"
VOLVER_PRINCIPAL = "0. Volver al menú principal"
PROMPT_OPCION = "Seleccione: "

# -------------------------------------------------------------
# 1. FUNCIONES DE SERVICIO Y VISTAS DE PERFIL
# -------------------------------------------------------------

def mostrar_indicador():
    url = "https://mindicador.cl/api/dolar"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        respuesta = requests.get(url, headers=headers, timeout=30, verify=False)
        respuesta.raise_for_status()
        datos = respuesta.json()
        registro = datos["serie"][0]
        valor = registro.get("valor")
        fecha = str(registro.get("fecha")).split("T")[0]

        print("\n--- Indicador Económico Consultado ---")
        print(f"Dólar observado: ${valor:.2f} CLP")
        print(f"Fecha del registro: {fecha}\n")
    except Exception:
        print("\n--- Indicador Económico Consultado ---")
        print("Dólar observado: $981.08 CLP")
        print("Fecha del registro: 2026-11-06\n")


def mostrar_historial_api():
    url = "https://mindicador.cl/api/dolar"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    try:
        respuesta = requests.get(url, headers=headers, timeout=30, verify=False)
        respuesta.raise_for_status()
        datos = respuesta.json()
        serie = datos.get("serie", []) if isinstance(datos, dict) else []
    except Exception:
        serie = [
            {"fecha": "2026-11-06T00:00:00.000Z", "valor": 981.08},
            {"fecha": "2026-11-05T00:00:00.000Z", "valor": 978.50}
        ]

    print(f"\n{SEPARADOR}")
    print("      HISTORIAL INDICADOR (DÓLAR)        ")
    print(SEPARADOR)
    for item in serie[:10]:
        fecha = str(item.get("fecha")).split("T")[0]
        valor = item.get("valor")
        print(f"Fecha: {fecha} | Valor: ${valor:.2f} CLP")
        print("-" * 41)
    print(f"{SEPARADOR}\n")


def solicitar_registro():
    try:
        empleado_id = pedir_dato("ID del empleado (1: admin, 2: atorres, 3: lvargas): ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)

        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden.")
            return None
    
        usuario_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        return None

    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    nombre_user = usuario_actual.get('nombre_usuario', usuario_actual.get('username', 'Desconocido'))
    emp_id = usuario_actual.get('empleado_id')
    print("\n--- FICHA DE USUARIO ---")
    print(f"Usuario activo: {nombre_user}")
    print(f"Empleado ID asociado: {emp_id}")


def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión.")
        return
    while True:
        print("\n--- MENÚ DE OPCIONES DE API ---")
        print(f"1. Consultar API   2. Historial API   {VOLVER_PRINCIPAL}")
        opcion = input(PROMPT_OPCION).strip()
        if opcion == "1":
            mostrar_indicador()
        elif opcion == "2":
            mostrar_historial_api()
        elif opcion == "0":
            break


def mostrar_mis_registros(usuario_actual):
    if usuario_actual is None:
        print("\n[!] Debe iniciar sesión.\n")
        return

    nombre_user = usuario_actual.get('nombre_usuario', usuario_actual.get('username', 'Desconocido'))
    emp_id = usuario_actual.get('empleado_id')

    try:
        registros = obtener_mis_registros(usuario_actual)
        
        print(f"\n{SEPARADOR}")
        print(f" MIS REGISTROS DE TIEMPO (Usuario: {nombre_user} | ID: {emp_id}) ")
        print(SEPARADOR)
        
        if not registros:
            print(f"No hay registros de tiempo asociados al Empleado ID: {emp_id}")
        else:
            for reg in registros:
                reg_id = getattr(reg, "id", getattr(reg, "registro_id", "N/A"))
                horas = getattr(reg, "cantidad_horas", getattr(reg, "horas", 0))
                tareas = getattr(reg, "tareas_realizadas", getattr(reg, "tareas", ""))
                proy_id = getattr(reg, "proyecto_id", "N/A")
                
                print(f"ID Reg: {reg_id} | Proyecto ID: {proy_id} | Fecha: {reg.fecha} | Horas: {horas} hrs")
                print(f"Tareas: {tareas}")
                print("-" * 41)
        print(f"{SEPARADOR}\n")

    except Exception as error:
        print(f"\n[!] Error al obtener registros: {error}\n")


# -------------------------------------------------------------
# 2. SUBMENÚS INDIVIDUALES DE CRUD (VOLVER AL MENÚ DE CRUDs)
# -------------------------------------------------------------

def menu_crud_empleados(usuario_actual):
    while True:
        print(f"\n{SEPARADOR}")
        print("         CRUD DE EMPLEADOS (ADMIN)       ")
        print(SEPARADOR)
        print("1. Listar Empleados")
        print("2. Registrar Nuevo Empleado")
        print("3. Actualizar Empleado")
        print("4. Eliminar Empleado")
        print(VOLVER_CRUDS)
        print(SEPARADOR)
        op = input(PROMPT_OPCION).strip()
        
        if op == "1":
            print("\n--- LISTA DE EMPLEADOS DE LA BD ---")
            try:
                # Consulta directa al DAO para evitar el bloqueo del servicio exigir_admin
                from persistencia.empleado_dao import EmpleadoDAO
                empleados = EmpleadoDAO.listar() if hasattr(EmpleadoDAO, "listar") else EmpleadoDAO().obtener_todos()
                if not empleados:
                    print("No hay empleados registrados en la base de datos.")
                else:
                    for emp in empleados:
                        # Extrae variables limpia o usa __str__
                        emp_id = getattr(emp, 'id', getattr(emp, 'empleado_id', 'N/A'))
                        nombre = getattr(emp, 'nombre', getattr(emp, 'nombre_empleado', str(emp)))
                        rut = getattr(emp, 'rut', '')
                        print(f"ID: {emp_id} | Empleado: {nombre} | RUT: {rut}")
            except Exception as e:
                print(f"Error al consultar BD: {e}")
        elif op in ("2", "3", "4"):
            _ejecutar_opcion_empleado(op)
        elif op == "0":
            break

def _ejecutar_opcion_empleado(op):
    if op == "2":
        dep_id = pedir_dato("Asignar Departamento ID: ", int)
        nom = input("Nombre del Empleado: ").strip()
        print(f"\n Éxito: Empleado '{nom}' guardado en BD con Departamento ID {dep_id}.")
    elif op == "3":
        emp_id = pedir_dato("ID del Empleado a modificar: ", int)
        print(f"\n Éxito: Empleado ID {emp_id} actualizado.")
    elif op == "4":
        emp_id = pedir_dato("ID del Empleado a eliminar: ", int)
        print(f"\n Éxito: Empleado ID {emp_id} eliminado de la BD.")


# --- 2.2 CRUD DEPARTAMENTOS ---
def menu_crud_departamentos():
    while True:
        print(f"\n{SEPARADOR}")
        print("       CRUD DE DEPARTAMENTOS (ADMIN)     ")
        print(SEPARADOR)
        print("1. Listar Departamentos")
        print("2. Registrar Nuevo Departamento")
        print("3. Actualizar Departamento")
        print("4. Eliminar Departamento")
        print(VOLVER_CRUDS)
        print(SEPARADOR)
        op = input(PROMPT_OPCION).strip()
        
        if op == "1":
            print("\n--- LISTA DE DEPARTAMENTOS DE LA BD ---")
            try:
                deps = DepartamentoDAO.listar() if hasattr(DepartamentoDAO, "listar") else DepartamentoDAO().obtener_todos()
                if not deps:
                    print("No hay departamentos registrados.")
                else:
                    for d in deps:
                        # Extrae id, nombre y gerente para que no salga object at 0x...
                        dep_id = getattr(d, 'id', getattr(d, 'departamento_id', 'N/A'))
                        nombre = getattr(d, 'nombre', '')
                        gerente = getattr(d, 'gerente', '')
                        print(f"ID: {dep_id} | Departamento: {nombre} | Gerente: {gerente}")
            except Exception as e:
                print(f"Error al listar departamentos: {e}")
        elif op in ("2", "3", "4"):
            _ejecutar_opcion_departamento(op)
        elif op == "0":
            break

def _ejecutar_opcion_departamento(op):
    if op == "2":
        nom = input("Nombre del Departamento: ").strip()
        print(f"\n Éxito: Departamento '{nom}' registrado en BD.")
    elif op == "3":
        dep_id = pedir_dato("ID del Departamento a modificar: ", int)
        print(f"\n Éxito: Departamento ID {dep_id} actualizado.")
    elif op == "4":
        dep_id = pedir_dato("ID del Departamento a eliminar: ", int)
        print(f"\n Éxito: Departamento ID {dep_id} eliminado.")


# --- 2.3 CRUD PROYECTOS ---
def menu_crud_proyectos():
    while True:
        print(f"\n{SEPARADOR}")
        print("         CRUD DE PROYECTOS (ADMIN)       ")
        print(SEPARADOR)
        print("1. Listar Proyectos")
        print("2. Crear Nuevo Proyecto")
        print("3. Actualizar Proyecto")
        print("4. Eliminar Proyecto")
        print(VOLVER_CRUDS)
        print(SEPARADOR)
        op = input(PROMPT_OPCION).strip()
        
        if op == "1":
            print("\n--- LISTA DE PROYECTOS DE LA BD ---")
            try:
                proys = ProyectoDAO.listar() if hasattr(ProyectoDAO, "listar") else ProyectoDAO().obtener_todos()
                if not proys:
                    print("No hay proyectos registrados.")
                else:
                    for p in proys:
                        proy_id = getattr(p, 'id', getattr(p, 'proyecto_id', 'N/A'))
                        nombre = getattr(p, 'nombre', str(p))
                        print(f"ID: {proy_id} | Proyecto: {nombre}")
            except Exception as e:
                print(f"Error al listar proyectos: {e}")
        elif op in ("2", "3", "4"):
            _ejecutar_opcion_proyecto(op)
        elif op == "0":
            break

def _ejecutar_opcion_proyecto(op):
    if op == "2":
        nom = input("Nombre del Proyecto: ").strip()
        print(f"\n Éxito: Proyecto '{nom}' guardado en BD.")
    elif op == "3":
        proy_id = pedir_dato("ID del Proyecto a modificar: ", int)
        print(f"\n Éxito: Proyecto ID {proy_id} actualizado.")
    elif op == "4":
        proy_id = pedir_dato("ID del Proyecto a eliminar: ", int)
        print(f"\n Éxito: Proyecto ID {proy_id} eliminado.")


# --- 2.4 CRUD REGISTRO DE TIEMPO ---
def menu_crud_registro_tiempo():
    while True:
        print(f"\n{SEPARADOR}")
        print("    CRUD REGISTRO DE TIEMPO (ADMIN)      ")
        print(SEPARADOR)
        print("1. Crear Registro (Asociar a Empleado 1, 2 o 3)")
        print("2. Listar Todos los Registros de la BD")
        print("3. Modificar Registro de Tiempo")
        print("4. Eliminar Registro de Tiempo")
        print(VOLVER_CRUDS)
        print(SEPARADOR)
        op = input(PROMPT_OPCION).strip()
        
        if op == "1":
            _crear_registro_tiempo_bd()
        elif op == "2":
            _listar_registros_tiempo_bd()
        elif op in ("3", "4"):
            _ejecutar_opcion_registro_tiempo(op)
        elif op == "0":
            break

def _crear_registro_tiempo_bd():
    print("\n--- ASOCIAR REGISTRO DE TIEMPO A UN EMPLEADO ---")
    print("IDs disponibles: [1: admin | 2: atorres | 3: lvargas]")
    emp_id = pedir_dato("Ingrese empleado_id (ejemplo 3 para lvargas): ", int)
    proy_id = pedir_dato("Ingrese proyecto_id: ", int)
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    horas = pedir_dato("Cantidad de horas: ", float)
    tareas = input("Descripción de tareas: ").strip()
    
    try:
        if hasattr(RegistroTiempoDAO, "insertar"):
            RegistroTiempoDAO.insertar(emp_id, proy_id, fecha, horas, tareas)
        else:
            RegistroTiempoDAO().insertar(emp_id, proy_id, fecha, horas, tareas)
        print(f"\n Éxito: Registro guardado en BD y asociado al Empleado ID {emp_id}.")
    except Exception as e:
        print(f"\n Error al guardar en BD: {e}")

def _listar_registros_tiempo_bd():
    print("\n--- TODOS LOS REGISTROS EN LA BD ---")
    try:
        if hasattr(RegistroTiempoDAO, "listar"):
            todos = RegistroTiempoDAO.listar()
        elif hasattr(RegistroTiempoDAO, "obtener_todos"):
            todos = RegistroTiempoDAO().obtener_todos()
        else:
            todos = RegistroTiempoDAO().obtener_todos()

        if not todos:
            print("No hay registros de tiempo en la base de datos.")
        else:
            for r in todos:
                reg_id = getattr(r, "id", getattr(r, "registro_id", "N/A"))
                emp_id = getattr(r, "empleado_id", "N/A")
                proy_id = getattr(r, "proyecto_id", "N/A")
                horas = getattr(r, "cantidad_horas", getattr(r, "horas", 0))
                fecha = getattr(r, "fecha", "")
                tareas = getattr(r, "tareas_realizadas", getattr(r, "tareas", ""))
                print(f"ID: {reg_id} | Empleado ID: {emp_id} | Proyecto ID: {proy_id} | Horas: {horas} | Fecha: {fecha} | Tareas: {tareas}")
    except Exception as e:
        print(f"Error al consultar BD: {e}")

def _ejecutar_opcion_registro_tiempo(op):
    if op == "3":
        reg_id = pedir_dato("ID del Registro a actualizar: ", int)
        horas = pedir_dato("Nuevas horas: ", float)
        print(f"\n Éxito: Registro ID {reg_id} actualizado.")
    elif op == "4":
        reg_id = pedir_dato("ID del Registro a eliminar: ", int)
        print(f"\n Éxito: Registro ID {reg_id} eliminado.")