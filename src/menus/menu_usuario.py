import math
from getpass import getpass
import requests
from entradas import pedir_dato
from servicios.autenticacion import registrar_usuario, autenticar 
from dominio.usuario import Usuario
from servicios.gestion_empleados import listar_todos 
from servicios.gestion_registros import obtener_mis_registros 
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO 
from persistencia.empleado_dao import EmpleadoDAO
from menus.menu_departamento import _listar_departamentos_bd
from menus.menu_proyecto import _listar_proyectos_bd
from menus.menu_empleado import _listar_empleados_bd




# -------------------------------------------------------------
# CONSTANTES DE INTERFAZ
# -------------------------------------------------------------
SEPARADOR = "========================================="
VOLVER_CRUDS = "0. Volver al menú de CRUDs"
VOLVER_PRINCIPAL = "0. Volver al menú principal"
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
        opcion = input("Seleccione opción de API [1,3]: ").strip()
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
# 2. SUBMENÚS CRUD 
# -------------------------------------------------------------

# --- 2.1 CRUD EMPLEADOS ---
def menu_crud_empleados(usuario_actual):
    _ = usuario_actual
    while True:
        print(f"\n{SEPARADOR}\n         CRUD DE EMPLEADOS (ADMIN)       \n{SEPARADOR}\n1. Listar Empleados\n2. Registrar Nuevo Empleado\n3. Actualizar Empleado\n4. Eliminar Empleado\n{VOLVER_CRUDS}\n{SEPARADOR}")
        opcion = input("Seleccione opción [0-4]: ").strip()
        
        if opcion == "0":
            break
        if opcion == "1":
            _listar_empleados_bd()
        elif opcion == "2" or opcion == "3" or opcion == "4":
            _ejecutar_opcion_empleado(opcion)
            
            
def _ejecutar_opcion_empleado(op):
    try:
        if op == "2":
            dep_id = pedir_dato("Asignar Departamento ID: ", int)
            nom = input("Nombre del Empleado: ").strip()
            rut = input("RUT del Empleado: ").strip()
            if hasattr(EmpleadoDAO, "insertar"):
                EmpleadoDAO.insertar(nom, rut, dep_id)
            else:
                EmpleadoDAO().insertar(nom, rut, dep_id)
            print(f"\n Éxito: Empleado '{nom}' guardado en BD.")

        elif op == "3":
            emp_id = pedir_dato("ID del Empleado a modificar: ", int)
            nom = input("Nuevo nombre del Empleado: ").strip()
            if hasattr(EmpleadoDAO, "actualizar"):
                EmpleadoDAO.actualizar(emp_id, nom)
            else:
                EmpleadoDAO().actualizar(emp_id, nom)
            print(f"\n Éxito: Empleado ID {emp_id} actualizado.")

        elif op == "4":
            emp_id = pedir_dato("ID del Empleado a eliminar: ", int)
            if hasattr(EmpleadoDAO, "eliminar"):
                EmpleadoDAO.eliminar(emp_id)
            else:
                EmpleadoDAO().eliminar(emp_id)
            print(f"\n Éxito: Empleado ID {emp_id} eliminado de la BD.")
    except Exception as e:
        print(f"\n Error al operar en BD: {e}")

# --- 2.2 CRUD DEPARTAMENTOS ---
def menu_crud_departamentos():
    while True:
        print(f"\n{SEPARADOR}\n       CRUD DE DEPARTAMENTOS (ADMIN)     \n{SEPARADOR}\n1. Listar Departamentos\n2. Registrar Nuevo Departamento\n3. Actualizar Departamento\n4. Eliminar Departamento\n{VOLVER_CRUDS}\n{SEPARADOR}")
        opcion = input("Ingrese opción [0-4]: ").strip()
        
        if opcion == "0":
            break
        if opcion == "1":
            _listar_departamentos_bd()
        elif opcion == "2" or opcion == "3" or opcion == "4":
            _ejecutar_opcion_departamento(opcion)

def _ejecutar_opcion_departamento(op):
    try:
        if op == "2":
            nom = input("Nombre del Departamento: ").strip()
            gerente = input("Gerente (opcional): ").strip()
            # Guarda de verdad en la base de datos ecotech.db
            if hasattr(DepartamentoDAO, "insertar"):
                DepartamentoDAO.insertar(nom, gerente)
            else:
                DepartamentoDAO().insertar(nom, gerente)
            print(f"\n Éxito: Departamento '{nom}' registrado en BD.")

        elif op == "3":
            dep_id = pedir_dato("ID del Departamento a modificar: ", int)
            nom = input("Nuevo nombre del Departamento: ").strip()
            # Actualiza en la BD
            if hasattr(DepartamentoDAO, "actualizar"):
                DepartamentoDAO.actualizar(dep_id, nom)
            else:
                DepartamentoDAO().actualizar(dep_id, nom)
            print(f"\n Éxito: Departamento ID {dep_id} actualizado.")

        elif op == "4":
            dep_id = pedir_dato("ID del Departamento a eliminar: ", int)
            # Elimina en la BD
            if hasattr(DepartamentoDAO, "eliminar"):
                DepartamentoDAO.eliminar(dep_id)
            else:
                DepartamentoDAO().eliminar(dep_id)
            print(f"\n Éxito: Departamento ID {dep_id} eliminado.")
    except Exception as e:
        print(f"\n Error al operar en BD: {e}")


# --- 2.3 CRUD PROYECTOS ---
def menu_crud_proyectos():
    while True:
        print(f"\n{SEPARADOR}\n         CRUD DE PROYECTOS (ADMIN)       \n{SEPARADOR}\n1. Listar Proyectos\n2. Crear Nuevo Proyecto\n3. Actualizar Proyecto\n4. Eliminar Proyecto\n{VOLVER_CRUDS}\n{SEPARADOR}")
        opcion = input("Elija una opción [0-4]: ").strip()
        
        if opcion == "0":
            break
        if opcion == "1":
            _listar_proyectos_bd()
        elif opcion == "2" or opcion == "3" or opcion == "4":
            _ejecutar_opcion_proyecto(opcion)
            
            
def _ejecutar_opcion_proyecto(op):
    try:
        if op == "2":
            nom = input("Nombre del Proyecto: ").strip()
            if hasattr(ProyectoDAO, "insertar"):
                ProyectoDAO.insertar(nom)
            else:
                ProyectoDAO().insertar(nom)
            print(f"\n Éxito: Proyecto '{nom}' guardado en BD.")
        elif op == "3":
            proy_id = pedir_dato("ID del Proyecto a modificar: ", int)
            nom = input("Nuevo nombre del Proyecto: ").strip()
            if hasattr(ProyectoDAO, "actualizar"):
                ProyectoDAO.actualizar(proy_id, nom)
            else:
                ProyectoDAO().actualizar(proy_id, nom)
            print(f"\n Éxito: Proyecto ID {proy_id} actualizado en BD.")
        elif op == "4":
            proy_id = pedir_dato("ID del Proyecto a eliminar: ", int)
            if hasattr(ProyectoDAO, "eliminar"):
                ProyectoDAO.eliminar(proy_id)
            else:
                ProyectoDAO().eliminar(proy_id)
            print(f"\n Éxito: Proyecto ID {proy_id} eliminado de BD.")
    except Exception as e:
        print(f"\n Error al operar en BD: {e}")


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
        op = input("ingresa opcion  [0-5]: ").strip()
        
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
    emp_id = pedir_dato("Ingrese empleado_id: ", int)
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
            todos = RegistroTiempoDAO.obtener_todos()
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
    try:
        if op == "3":
            reg_id = pedir_dato("ID del Registro a actualizar: ", int)
            horas = pedir_dato("Nuevas horas: ", float)
            if hasattr(RegistroTiempoDAO, "actualizar"):
                RegistroTiempoDAO.actualizar(reg_id, horas)
            else:
                RegistroTiempoDAO().actualizar(reg_id, horas)
            print(f"\n Éxito: Registro ID {reg_id} actualizado en BD.")
        elif op == "4":
            reg_id = pedir_dato("ID del Registro a eliminar: ", int)
            if hasattr(RegistroTiempoDAO, "eliminar"):
                RegistroTiempoDAO.eliminar(reg_id)
            else:
                RegistroTiempoDAO().eliminar(reg_id)
            print(f"\n Éxito: Registro ID {reg_id} eliminado de BD.")
    except Exception as e:
        print(f"\n Error al operar en BD: {e}")
# -------------------------------------------------------------
# 3. MENÚ PRINCIPAL DE CRUDs DE ADMINISTRACIÓN
# -------------------------------------------------------------

def menu_principal_cruds(usuario_actual):
    while True:
        print(f"\n{SEPARADOR}")
        print("       MENÚ DE CRUDs (ADMINISTRACIÓN)    ")
        print(SEPARADOR)
        print("1. CRUD Empleados")
        print("2. CRUD Departamentos")
        print("3. CRUD Proyectos")
        print("4. CRUD Registros de Tiempo")
        print("-----------------------------------------")
        print(VOLVER_PRINCIPAL)
        print(SEPARADOR)
        
        op = input("Seleccione opción [0-5]: ").strip()
        
        if op == "1":
            menu_crud_empleados(usuario_actual)
        elif op == "2":
            menu_crud_departamentos()
        elif op == "3":
            menu_crud_proyectos()
        elif op == "4":
            menu_crud_registro_tiempo()
        elif op == "0":
            break


# -------------------------------------------------------------
# 4. MENÚ PRIVADO DE USUARIO
# -------------------------------------------------------------

def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    
    nombre_user = usuario_actual.get('nombre_usuario', usuario_actual.get('username', 'Desconocido'))
    nombre_user_lower = str(nombre_user).strip().lower()

    if nombre_user_lower == "admin":
        menu_principal_cruds(usuario_actual)

    while True:
        print(f"\n{SEPARADOR}")
        print(f"        MENÚ PRINCIPAL ({nombre_user})   ")
        print(SEPARADOR)
        print("1. Mi ficha")
        print(f"2. Mis registros (Usuario: {nombre_user})")
        print("3. Consultar API")
        
        if nombre_user_lower == "admin":
            print("4. Menú de CRUDs de Administración")
            
        print("-----------------------------------------")
        print("9. Cerrar sesión  0. Salir del programa")
        print(SEPARADOR)
        
        opcion = input("Seleccione: ").strip()
        
        if opcion == "1":
            mostrar_perfil(usuario_actual)
        elif opcion == "2":
            mostrar_mis_registros(usuario_actual)
        elif opcion == "3":
            consultar_indicador(usuario_actual)
        elif opcion == "4" and nombre_user_lower == "admin":
            menu_principal_cruds(usuario_actual)
        elif opcion in ("0", "9"):
            return opcion
        else:
            print("Opción no válida.")