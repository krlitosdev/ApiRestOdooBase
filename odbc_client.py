import pyodbc
import sqlalchemy as db 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from settings import settings
from logger_config import logger

class SQLServerBaseConnection():
    def __init__(self): 
        self.message_execption_connection = None     
        self.engine = None  
        self.conn = None  
        if settings.debug:
            self.host_sqlserver = str(settings.dev_host_sqlserver)
            self.port_sqlserver = str(settings.dev_port_sqlserver)
            self.db_sqlserver = str(settings.dev_db_sqlserver)
            self.user_sqlserver = str(settings.dev_user_sqlserver)
            self.password_sqlserver = str(settings.dev_password_sqlserver)
        else:
            self.host_sqlserver = str(settings.prod_host_sqlserver)
            self.port_sqlserver = str(settings.prod_port_sqlserver)
            self.db_sqlserver = str(settings.prod_db_sqlserver)
            self.user_sqlserver = str(settings.prod_user_sqlserver)
            self.password_sqlserver = str(settings.prod_password_sqlserver)
                
        print('-> Comprobando conexion ',self.connect_to_db())
        
    
    def connect_to_db(self):
        try:
            self.engine = db.create_engine("mssql+pyodbc://{0}:{1}@{2}:{3}/{4}?driver=ODBC+Driver+17+for+SQL+Server&charset=utf8".format(
                self.user_sqlserver, self.password_sqlserver, self.host_sqlserver, self.port_sqlserver, self.db_sqlserver
            ), echo=True) 
            # Intentar conectar
            self.conn = self.engine.connect()  
            
            # Consultar los campos de todas las tablas
            #table_name = "cliente"
            #query = text(f"SELECT * FROM dbo.{table_name}")  # Usar text() para interpretar el SQL
            #result = self.conn.execute(query)
            #print("Lista de columnas en la base de datos:")
            #for row in result:
            #   print(row)
            # Cerrar la conexión
            #self.conn.close()
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al conectar a la base de datos [{self.db_sqlserver}] , Host: [{self.host_sqlserver}], Port: [{self.port_sqlserver}], Usuario: [{self.user_sqlserver}], Password: [*****]. Error : [{e}]")
            return False
        
        

sqlserver_bridge = SQLServerBaseConnection()