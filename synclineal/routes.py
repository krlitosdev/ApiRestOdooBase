from fastapi import APIRouter, Depends, status, Header, Request
from fastapi.exceptions import HTTPException
from logger_config import logger
from pydantic import BaseModel
from datetime import datetime
from utils import RequestFormaterLogsStr
from odoo_client import odoo_bridge
from .controllers.ClientController import bridge_client_controller

controllers =[
    bridge_client_controller
    ] 

synclineal_router = APIRouter()

class RequestModel(BaseModel):
    id: int
    tipo_persona_id: list[int] | None = [1,2,3,4]
   

@synclineal_router.post("/")
async def SyncLinealPost(request: Request,
                         item: RequestModel,client_name_header: str | None = Header(default="SyncLineal", convert_underscores=False),
                         id_event_header: str | None = Header(default="TestSyncLineal", convert_underscores=False)):
   
    #Detalles del Request
    request_url = str(request.url)  # URL de la petición
    request_client_ip, request_client_port = request.client # Una tupla que contiene la IP y el puerto del cliente.
    request_method = request.method  # Método HTTP (GET, POST, etc.)
    request_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Fecha de peticion de la solicitud    
    RequestFormaterLogsStr(request_url, request_method, request_client_ip, request_client_port, client_name_header, id_event_header,item.id,item.tipo_persona_id, request_datetime )
    
    for controller in controllers:
        controller.inicializar_datos(item.id,item.tipo_persona_id)
        controller.get_person_res_partner_data()
    
    return {"Haciendo": "Post"}