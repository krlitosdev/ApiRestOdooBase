from fastapi import APIRouter, Depends, status, Header, Request
from fastapi.exceptions import HTTPException
from logger_config import logger
from pydantic import BaseModel
from datetime import datetime
from utils import RequestFormaterLogsStr
from odoo_client import odoo_bridge
from .controllers.ClientController import bridge_client_controller
from .controllers.TestController import bridge_test_controller
from .controllers.TestController2 import bridge_test2_controller

# Agregar object controller en localdb_cliente
from localdb_client import bridge_local_db
from settings import settings
import asyncio
import time

controllers =[
    bridge_client_controller,
    bridge_test_controller,
    bridge_test2_controller
    ] 

synclineal_router = APIRouter()

class RequestModel(BaseModel):
    id: int
    tipo_persona_id: list[int] | None = [1,2,3,4]

def execute_controller_sync(controller, id, tipo_persona_id):
    """Ejecuta las funciones de un controlador de manera síncrona."""
    controller.inicializar_datos(id, tipo_persona_id)
    controller.get_person_res_partner_data()
    controller.sleepFunction()


@synclineal_router.post("/")
async def SyncLinealPost(request: Request,
                         item: RequestModel,client_name_header: str | None = Header(default="SyncLineal", convert_underscores=False),
                         id_event_header: str | None = Header(default="TestSyncLineal", convert_underscores=False)):
   
    inicio = time.time()
    
    #for controller in controllers:
    #    controller.inicializar_datos(item.id,item.tipo_persona_id)
    #    controller.get_person_res_partner_data()
    #    controller.sleepFunction()
        
    #return {"Haciendo": "Post"}

    results = []
    batch_size = int(settings.batch_size)
    # Procesar controladores simultaneos
    for i in range(0, len(controllers), batch_size):
        group = controllers[i:i + batch_size]

        # Crear tareas para ejecutar funciones bloqueantes en hilos
        tasks = [
            asyncio.to_thread(execute_controller_sync, controller, item.id, item.tipo_persona_id) 
            for controller in group
        ]

        # Ejecutar el grupo de tareas de manera concurrente
        group_results = await asyncio.gather(*tasks, return_exceptions=True)

        # Manejar resultados y excepciones
        for result in group_results:
            if isinstance(result, Exception):
                results.append({"status": "error", "message": str(result)})
            else:
                results.append({"status": "success"})
                
    # Medir el tiempo después de la ejecución
    fin = time.time()
    print(f"-> La ejecución de SyncLinealPost se demoró {fin - inicio:.2f} segundos.")
    return {"status": "completed", "results": results}