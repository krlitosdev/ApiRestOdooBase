from .BaseController import Base
from odoo_client import odoo_bridge
import time

class TestController2(Base):
    def __init__(self):
        super().__init__()
    
    def sleepFunction(self):
        print("-----> Inicio de la función TestController2")
        time.sleep(10)  # Pausa de 5 segundos
        print("-----> Fin de la función TestController2 después de 10 segundos.")

       

bridge_test2_controller =TestController2()