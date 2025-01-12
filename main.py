from typing import Union
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger_config import logger
from settings import settings
from synclineal.routes import synclineal_router

from odoo_client import odoo_bridge
from odbc_client import sqlserver_bridge

# Para el sistema de plantillas
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


version = "v1"
description = """
A REST API for a Empresa review web service.

This REST API is able to;
- Create Read Update And delete elements
- Add reviews to elements
- Add tags to elements e.t.c.
    """
version_prefix =f"/api/{version}"



@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando el Servicio")
    if settings.debug is True:
        logger.info("Modo Desarrollador activado [Para desabilitar el modo desarrollador cambie la variable 'DEBUG' en el archivo .env]")
    logger.info("Comprobando conexion a Odoo")    
    odoo_bridge.Check_Connection()
    logger.info("Comprobando conexion a SQL_Server")
    #logger.info("Comprobando conexion a Local DataBase")
    yield  # Este `yield` es necesario para que el ciclo de vida funcione correctamente
    logger.info("Finalizando el Servicio")
    

# Creando instancia de FastApi
app = FastAPI(
    title=settings.app_name,
    description=description,
    version=version,
     contact={
        "name": "Carlos",
        "url": "https://github.com/",
        "email": "useremail@gmail.com",
    },
    terms_of_service="httpS://example.com/tos",
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc",
    lifespan=lifespan
    )

# Host que pueden acceder a los puntos de accesos
origins = [
    "*",
]

# Cors Header Middleware Configuraciones
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(synclineal_router, prefix=f"{version_prefix}/synclineal", tags=["synclineal"])

# Ruta para el sistema de archivos estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2 para renderizar plantillas
templates = Jinja2Templates(directory="templates")

# Ruta base para la plantilla
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
    }