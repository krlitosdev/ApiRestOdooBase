from odoo_client import odoo_bridge
from logger_config import logger
from model import ClienteResPartner

class Base:
    def __init__(self):
        # Inicializar variables en la clase base
        self.id_person = None
        self.tipo_persona_ids = None

    def inicializar_datos(self, id_person, tipo_persona_ids):
        # Método para inicializar los datos
        self.id_person = id_person
        self.tipo_persona_ids = tipo_persona_ids
    
    def get_person_res_partner_async_data(self):
        pass
    
    def get_person_res_partner_data(self):
        logger.info(f"Buscando datos del cliente con ID [{self.id_person}] en la Base de datos de Odoo, en la tabla ['res.partner']")
        request_search_status,request_search_value=odoo_bridge.Search_Client('res.partner','id',self.id_person)
        if request_search_status is True: 
            logger.info(f"Buscando cliente en la tabla [res.partner] con ID [{str(request_search_value)}]")          
            request_get_client_status,request_get_client_value = odoo_bridge.Get_Client('res.partner',int(request_search_value),['id','name','company_id','create_date','display_name','date','title','parent_id','ref','lang','tz','user_id','vat','website','comment','credit_limit','active','employee','function','type','street','street2','zip','city','state_id','country_id','partner_latitude','partner_longitude','email','phone','mobile','is_company','industry_id','color','partner_share','commercial_partner_id','commercial_company_name','company_name','create_uid','write_uid','write_date','message_main_attachment_id','email_normalized','message_bounce','signup_type','signup_expiration','signup_token','calendar_last_notif_ack','team_id','partner_gid','additional_info','phone_sanitized','debit_limit','last_time_entries_checked','invoice_warn','invoice_warn_msg','supplier_rank','customer_rank','picking_warn','picking_warn_msg','sale_warn','sale_warn_msg','l10n_latam_identification_type_id'])
            if request_get_client_status is True:
                cliente = ClienteResPartner()
                cliente.cargar_datos(request_get_client_value[0])
                print(cliente.name)
                print(cliente.id)
                #print(cliente.active)
                return cliente
        return None
