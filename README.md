EcoTech Solutions - Evaluación 3

Descripción del proyecto

EcoTech Solutions es un proyecto desarrollado en Python para gestionar información de empleados, departamentos, proyectos y registros de tiempo. Su objetivo es organizar la información y facilitar las operaciones mediante el uso de clases, patrón DAO (Data Access Object) y una conexión a una base de datos, integrando además consumo de APIs externas y autenticación segura.

Tecnologías utilizadas

Lenguaje: Python (3.10+)

Bases de Datos: SQLite / MySQL

Control de Versiones: Git y GitHub

Librerías externas: requests (para API externa), bcrypt (cifrado de contraseñas), python-dotenv.

Guía Técnica de Inicialización

A continuación, se detallan los pasos exactos para configurar el entorno local, instalar las dependencias y ejecutar correctamente el sistema.

1. Creación y Activación del Entorno Virtual

Es altamente recomendado utilizar un entorno virtual para aislar las dependencias del proyecto.

Crear el entorno virtual:

python -m venv venv


Activar el entorno virtual:

En Windows:

venv\Scripts\activate


En macOS / Linux:

source venv/bin/activate

si trae errores al activar el entorno se ocupara el siguiente comando: 
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser


2. Instalación de Dependencias

Con el entorno virtual activo, instala las librerías requeridas utilizando el archivo de requerimientos ubicado en la raíz del proyecto.

pip install -r requirements.txt


3. Ejecución del Sistema

El código fuente principal se encuentra dentro de la carpeta src. Debes navegar a ese directorio antes de iniciar la base de datos o la aplicación.

 Ingresar a la carpeta 

cd src

python main.py


4. Solución de Errores Comunes (Base de Datos)

Si al ejecutar python main.py ocurre un error relacionado con la base de datos (por ejemplo, conflictos de esquema o registros duplicados), sigue estos pasos:

Detén la ejecución del programa (Ctrl + C).

Borra el archivo físico de la base de datos local (el archivo .db generado dentro de la carpeta).

Vuelve a ejecutar el archivo principal para que el sistema regenere la base de datos limpia desde cero:

python main.py