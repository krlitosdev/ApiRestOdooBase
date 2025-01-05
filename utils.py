from logger_config import logger

def RequestFormaterLogsStr(request_url, request_method, request_client_ip, request_client_port, client_name_header, id_event_header,id_person,tipo_persona_ids, request_datetime):
    message = "Url_request: {0} - Method: {1} - Cliente_IP: {2} - Cliente_Port: {3} - Cliente_Nombre: {4} - Id_Evento: {5} - ID_Persona: {6} - Tipos_Personas: {7} - Fecha_request: {8} ".format(request_url, request_method, request_client_ip, request_client_port, client_name_header, id_event_header,str(id_person),str(tipo_persona_ids), request_datetime)
    logger.info(message)