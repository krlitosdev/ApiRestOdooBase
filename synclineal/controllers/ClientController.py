from .BaseController import Base
from odoo_client import odoo_bridge

class ClientController(Base):
    def __init__(self):
        super().__init__()

bridge_client_controller =ClientController()