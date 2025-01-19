# Ejecutar servidor
fastapi run main.py

# New Changes
    - Crear el archivo "localdb_client.py" para establecer la conexion con la base de datos local que almacena los logs y trazas del sistema
    - Agregar las configuraciones de postgres al archivo .env
    - Agregar las variables de entorno al archivo settings.py 
    - Instalar los paquetes "pip install asyncpg psycopg2"
    - Agregar al archivo "logger_config.py" las importaciones y los metodos 
    - Agregar al archivo "main.py" las importaciones y los metodos "app.add_middleware(SlugMiddleware)" del "logger_config.py"
    - Eliminar el metodo RequestFormaterLogsStr() del archivo "utils.py" ya no hace falta.
    -  Agregar el path get_logs_with_alerts() al archivo main.py

# Configurando asyncio
    - Importar "import asyncio" en el archivo routes.py
    - Agregar el metodo execute_controller_sync(controller, id, tipo_persona_id) al archivo "routes.py" , asegurarse de los parametros que se le pasan al metodo
    - Añadir el resto del codigo al metodo SyncLinealPost() en el archivo "routes.py"
    - Agregar la variable "batch_size" en el .env
    - Agregar la variable "batch_size" en el "settings.py"
    - Agregar la variable "batch_size" en el "routes.py"

# Basic Auth
    - Agregamos los imports "from fastapi import Depends, HTTPException, status
                             from fastapi.security import HTTPBasic, HTTPBasicCredentials"
    - Crear una instancia de HTTPBasic "security = HTTPBasic()" en el archivo main.py
    - Crear una función de validación para la autenticación "validate_credentials" en el archivo main.py
    - Usar la validación en el endpoint específico "get_logs_with_alerts(credentials: HTTPBasicCredentials = Depends(validate_credentials)):" en el archivo "main.py"
