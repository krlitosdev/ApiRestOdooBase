from xmlrpc import client
from settings import settings
from logger_config import logger


class OdooBaseConnection():
    def __init__(self):     
        self.uid = None         
        self.message_execption_connection = None         
        if settings.debug:
            self.url_odoo = str(settings.dev_url_odoo)
            self.db_odoo = str(settings.dev_db_odoo)
            self.user_odoo = str(settings.dev_user_odoo)
            self.password_odoo = str(settings.dev_password_odoo)
        else:
            self.url_odoo = str(settings.prod_url_odoo)
            self.db_odoo = str(settings.prod_db_odoo)
            self.user_odoo = str(settings.prod_user_odoo)
            self.password_odoo = str(settings.prod_password_odoo)
        
        self.model = client.ServerProxy('{}/xmlrpc/2/object'.format(self.url_odoo))         
        try:
            common = client.ServerProxy('{}/xmlrpc/2/common'.format(self.url_odoo))
            res = common.version()
            uid = common.authenticate(self.db_odoo, self.user_odoo, self.password_odoo, {})            
            if uid:
                self.uid=uid
        except Exception as e:
            self.message_execption_connection = f"Error de conexion con el sistema Odoo: {str(e)}"   
    
    def Check_Connection(self):
        if self.uid:
            logger.info(f"Autenticacion exitosa con el Sistema Odoo. ID de usuario: {self.uid}")
            return True
        else:
            logger.error(self.message_execption_connection)
            logger.error(f"Host_Odoo: [{str(self.url_odoo)}] - User_Odoo: [{str(self.user_odoo)}] - Password_Odoo: [{str(self.password_odoo)}] - DB_Odoo: [{str(self.db_odoo)}] ")
            return False
    
    def Reconnect_Client(self):
        try:
            common = client.ServerProxy('{}/xmlrpc/2/common'.format(self.url_odoo))
            uid = common.authenticate(self.db_odoo, self.user_odoo, self.password_odoo, {})            
            if uid:
                self.uid=uid
        except Exception as e:
            self.message_execption_connection = f"Error de conexion con el sistema Odoo: {str(e)}" 
        
    
    def get_uid_user(self):
        return self.uid
    
    def Search_Client(self,tbl_name,field_name,field_value):        
        if self.uid is None:
            self.Reconnect_Client()
        try:            
            user_ids = self.model.execute_kw(self.db_odoo, self.uid, self.password_odoo, str(tbl_name), 'search',[[[str(field_name), '=', str(field_value)]]])
            return True,user_ids[0]
        except Exception as e:
            logger.warning(f"No se encontro ningun cliente con el id [{str(field_value)}] en la tabla [{str(tbl_name)}]. Es probable que este cliente no se encuentre en la base de datos o se encuentre con el campo [active=false]. Error: [{str(e)}]")
            return False, str(e)
    
    def Get_Client(self,tbl_name,id_value,fields_names):        
        if self.uid is None:
            self.Reconnect_Client()
        try:
            current_data = self.model.execute_kw(self.db_odoo, self.uid, self.password_odoo, str(tbl_name),'read',[[int(id_value)],fields_names])
            return True,current_data
        except Exception as e:
            logger.warning(f"No se encontro ningun cliente con el id [{str(id_value)}] en la tabla [{str(tbl_name)}]. Error: [{str(e)}]")
            return False, str(e)
    
            
            
        

odoo_bridge = OdooBaseConnection()