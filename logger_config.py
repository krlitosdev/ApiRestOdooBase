import logging
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from localdb_client import bridge_local_db
from threading import local

_thread_local = local()

class SlugMiddleware(BaseHTTPMiddleware):
    """Middleware para manejar slugs únicos por solicitud y registrar el log inicial en la base de datos."""
    def __init__(self, app):
        super().__init__(app)

        # Handler personalizado para capturar los logs y hacer un print dentro de SlugMiddleware
        self.log_capture_handler = LogCaptureHandler()
        self.log_capture_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(self.log_capture_handler)

    async def dispatch(self, request: Request, call_next):
        # Generar slug único usando LocalDBBaseConnection
        slug = bridge_local_db.generate_unique_slug()
        setattr(_thread_local, "slug", slug)

        # Log inicial (request principal)
        body = await request.body()
        log_data = {
            "host": request.client.host,
            "request": f"{request.method} {request.url}",
            "headers": dict(request.headers),
            "body": body.decode() if body else "",
            "slug": slug,
        }

        # Insertar el log principal (request) en la base de datos
        bridge_local_db.insert_request_log(
            slug=slug,
            request_type=request.method,
            host=request.client.host,
            request=str(request.url),
            header=json.dumps(dict(request.headers)),
            body=body.decode() if body else ""
        )

        # Registrar el log principal
        logger.info(json.dumps(log_data))

       
        response = await call_next(request)
        return response


log_file = "app.log"
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(slug)s - %(message)s'))
file_handler.setLevel(logging.INFO)

logger = logging.getLogger("structured_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)


def get_current_slug():
    """Obtiene el slug actual del contexto del middleware."""
    return getattr(_thread_local, "slug", "unknown_slug")


class SlugFilter(logging.Filter):
    """Filtro para agregar el slug activo a todos los logs secundarios."""
    def filter(self, record):
        record.slug = get_current_slug()
        return True


# Añadimos el filtro para obtener el slug activo en los logs secundarios
logger.addFilter(SlugFilter())


# Handler personalizado para capturar los logs y hacer un print
class LogCaptureHandler(logging.Handler):
    def emit(self, record):
        # Obtener el tipo de log y el mensaje
        log_type = record.levelname  # INFO, WARNING, ERROR
        message = self.format(record)  # El mensaje que se pasa a logger.info() u otros
        is_parent = False
        try:
            data = json.loads(message)       
            host_value = data.get('host')
            if host_value is not None or len(host_value)>0:
                is_parent=True
        except:
            pass
        
        # Insertar el log en la base de datos si es un log hijo
        if log_type in ['INFO', 'ERROR', 'WARNING'] and is_parent is False:  # Solo insertamos ciertos tipos de log
            bridge_local_db.insert_logger_message(record.slug, message,str(log_type))