from .BaseController import Base
from odoo_client import odoo_bridge
import time

class ClientController(Base):
    def __init__(self):
        super().__init__()
    
    def sleepFunction(self):
        print("-----> Inicio de la función (ClientController).")
        time.sleep(10)  # Pausa de 5 segundos
        print("-----> Fin de la función (ClientController) después de 5 segundos.")

       

bridge_client_controller =ClientController()