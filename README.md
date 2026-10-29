EcoTech Solutions - Evaluación 3

Descripción del proyecto

EcoTech Solutions es un proyecto desarrollado en Python para gestionar información de empleados, departamentos, proyectos y registros de tiempo. Su objetivo es organizar la información y facilitar las operaciones mediante el uso de clases, patrón DAO (Data Access Object) y una conexión a una base de datos, integrando además consumo de APIs externas y autenticación segura.

Tecnologías utilizadas

Lenguaje: Python (3.10+)

Bases de Datos: SQLite / MySQL

Control de Versiones: Git y GitHub

Librerías externas: requests (para API externa), bcrypt (cifrado de contraseñas), python-dotenv.

Guía Técnica de Inicialización (Git Bash / Linux / macOS)

A continuación, se detallan los pasos exactos para configurar el entorno local, instalar las dependencias y ejecutar correctamente el sistema utilizando la terminal Git Bash.

1. Creación y Activación del Entorno Virtual

Crear el entorno virtual (usando .venv):

python -m venv .venv


Activar el entorno virtual:

source .venv/Scripts/activate


(Deberás ver (.venv) al inicio de la línea en tu terminal, indicando que está activo).

Abrir el proyecto en el editor de código:
code .


2. Instalación de Dependencias

Con el entorno virtual activo, instala las librerías requeridas utilizando el archivo de requerimientos ubicado en la raíz del proyecto.

pip install -r requirements.txt


3. Ejecución del Sistema

El código fuente principal se encuentra dentro de la carpeta src. Debes navegar a ese directorio antes de iniciar la carga de datos o la aplicación.

Ingresar a la carpeta fuente:

cd src


Cargar base de datos inicial (incluye creación de usuario administrador):

python semilla_bd.py


Iniciar la aplicación principal:

python main.py


4. Solución de Errores Comunes (Base de Datos)

Si al ejecutar python main.py ocurre un error relacionado con la base de datos (por ejemplo, sqlite3.OperationalError: database is locked, conflictos de esquema o registros duplicados), sigue estos pasos:

Detén la ejecución del programa (Ctrl + C).

Estando dentro de la carpeta src, borra el archivo físico de la base de datos local (el archivo .db o .sqlite generado).

Vuelve a cargar las semillas y ejecutar el archivo principal para que el sistema regenere la base de datos limpia desde cero:

python semilla_bd.py
python main.py