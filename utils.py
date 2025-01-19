from logger_config import logger

def RequestFormaterLogsStr(request):
    message = {
        "type": "parent",
        "event": "request",
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "client": request.client.host
    }
    logger.info(message)