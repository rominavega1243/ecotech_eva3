import re
from datetime import datetime
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO


def registrar_empleado():
    while True:
        nombre = input("Nombre: ").strip()
        if nombre.replace(" ", "").isalpha() and len(nombre) <= 10:
            break
        print("Error: El nombre solo puede contener 10 palabras.")

    while True:
        correo = input("Correo: ").strip()
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo) and correo.endswith("@ecotech.com"):
            break
        print("Error: Formato inválido. Ejemplo: usuario@ecotech.com")

    while True:
        telefono = input("Teléfono: ").strip()
        if telefono.isdigit() and len(telefono) >= 8:
            break
        print("Error: El teléfono debe contener solo números (mínimo 8).")

    while True:
        fecha_inicio_contrato = input("Fecha de inicio de contrato (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha_inicio_contrato, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Formato de fecha incorrecto. Use YYYY-MM-DD.")

    while True:
        try:
            salario = float(input("Salario: ").strip())
            if salario > 0:
                break
            print("Error: El salario debe ser mayor a 0.")
        except ValueError:
            print("Error: El salario debe ser numérico.")

    empleado = Empleado(
        nombre=nombre, 
        correo=correo, 
        telefono=telefono, 
        fecha_inicio_contrato=fecha_inicio_contrato, 
        salario=salario
    )
    
    try:
        EmpleadoDAO.insertar(empleado)
        print("Empleado registrado correctamente.")
    except Exception as e:
        print(f"No fue posible registrar el empleado: {e}")


def _listar_empleados_bd():
    empleados = EmpleadoDAO.listar()
    if empleados:
        print("\nLista de empleados:")
        for emp in empleados:
            print(f"ID: {emp.id}, Nombre: {emp.nombre}, Correo: {emp.correo}, Teléfono: {emp.telefono}, Salario: {emp.salario}")
    else:
        print("No hay empleados registrados.")


def buscar_empleado():
    id_empleado = input("Ingrese el ID del empleado a buscar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado:
        print(f"ID: {empleado.id}, Nombre: {empleado.nombre}, Correo: {empleado.correo}, Teléfono: {empleado.telefono}, Salario: {empleado.salario}")
    else:
        print("No se encontró al empleado buscado.")


def actualizar_empleado():
    id_empleado = input("Ingrese el ID del empleado a actualizar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if not empleado:
        print("Empleado no existe para actualizar.")
        return

    nombre = input(f"Nombre ({empleado.nombre}): ").strip()
    if nombre:
        empleado.nombre = nombre

    correo = input(f"Correo ({empleado.correo}): ").strip()
    if correo:
        empleado.correo = correo

    telefono = input(f"Teléfono ({empleado.telefono}): ").strip()
    if telefono:
        empleado.telefono = telefono

    fecha_inicio_contrato = input(f"Fecha de inicio ({empleado.fecha_inicio_contrato}): ").strip()
    if fecha_inicio_contrato:
        empleado.fecha_inicio_contrato = fecha_inicio_contrato

    salario_str = input(f"Salario ({empleado.salario}): ").strip()
    if salario_str:
        try:
            empleado.salario = float(salario_str)
        except ValueError:
            print("Error: El salario debe ingresarse como número.")

    try:
        EmpleadoDAO.actualizar(empleado)
        print("Empleado actualizado correctamente.")
    except Exception as e:
        print(f"Error al actualizar empleado: {e}")


def eliminar_empleado():
    id_empleado = input("Ingrese el ID del empleado a eliminar: ").strip()
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado:
        confirmacion = input(f"¿Seguro que desea eliminar al empleado {empleado.nombre}? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                EmpleadoDAO.eliminar(id_empleado)
                print("Empleado eliminado correctamente.")
            except Exception as e:
                print(f"No existe el empleado a eliminar: {e}")
        else:
            print("Eliminación cancelada.")
    else:
        print("Empleado no encontrado.")


def menu_empleado():
    print("\n===== ECOTECH - EMPLEADOS =====")
    print("1. Registrar empleado")
    print("2. Listar empleados")
    print("3. Buscar empleado")
    print("4. Actualizar empleado")
    print("5. Eliminar empleado")
    print("0. Salir")


def ejecutar_menu():
    while True:
        menu_empleado()
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            registrar_empleado()
        elif opcion == "2":
            _listar_empleados_bd()
        elif opcion == "3":
            buscar_empleado()
        elif opcion == "4":
            actualizar_empleado()
        elif opcion == "5":
            eliminar_empleado()
        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")