import sqlalchemy as db
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from settings import settings
import random
import string

Base = declarative_base()

class RequestLogger(Base):
    __tablename__ = 'requestlogger'

    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False, unique=True)
    request_type = Column(String(100), nullable=False)
    host = Column(String(100), nullable=False)
    request = Column(String(250), nullable=False)
    header = Column(Text, nullable=False)  # Cambiado de String(500) a Text
    body = Column(Text, nullable=False)    # Cambiado de String(500) a Text
    created_on = Column(DateTime(), default=datetime.now)

class LoggerMessage(Base):
    __tablename__ = 'loggermessage'

    id = Column(Integer(), primary_key=True)
    slug = Column(String(100), nullable=False) # Relación con el log principal
    log_type = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)    
    created_on = Column(DateTime(), default=datetime.now)

class LocalDBBaseConnection:
    def __init__(self):
        self.host = str(settings.local_host_postgres)
        self.port = str(settings.local_port_postgres)
        self.db = str(settings.local_db_postgres)
        self.user = str(settings.local_user_postgres)
        self.password = str(settings.local_password_postgres)
        
        DATABASE_URL = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"
        self.engine = create_engine(DATABASE_URL, echo=True, pool_size=20, max_overflow=0)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
        # Crear las tablas al inicializar la clase
        self.create_tables()
    
    def create_tables(self):
        """Crea las tablas definidas en el modelo si no existen."""
        Base.metadata.create_all(self.engine)
    
    def check_connection(self):
        """Verifica si la conexión con la base de datos se establece correctamente."""
        try:
            with self.engine.connect() as connection:
                connection.execute(db.text("SELECT 1"))
            return True
        except SQLAlchemyError as e:
            print(f"Error al verificar la conexión: {e}")
            return False

    def check_character(self, character):
        """Verifica si el character (slug) ya existe en la tabla `requestlogger`."""
        session = self.SessionLocal()
        try:
            result = session.query(RequestLogger).filter(RequestLogger.slug == character).first()
            return result is not None
        except SQLAlchemyError as e:
            print(f"Error al verificar el slug: {e}")
            return False
        finally:
            session.close()
    
    def generate_unique_slug(self):
        """Genera un slug único verificando que no exista en la base de datos."""
        characters = string.ascii_lowercase + string.digits
        slug = ""
        while True:
            slug = ''.join(random.choice(characters) for _ in range(20))
            if not self.check_character(slug):
                break
        return slug

    def insert_request_log(self, slug, request_type, host, request, header, body):
        """Inserta un nuevo registro en la tabla `requestlogger`."""
        session = self.SessionLocal()
        try:
            new_request = RequestLogger(
                slug=slug,
                request_type=request_type,
                host=host,
                request=request,
                header=header,
                body=body
            )
            session.add(new_request)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al crear el registro: {e}")
        finally:
            session.close()

    def insert_logger_message(self, slug, message,log_type):
        """Inserta un mensaje de log hijo en la tabla `loggermessage`."""
        session = self.SessionLocal()
        try:
            new_message = LoggerMessage(
                slug=slug,
                message=message,
                log_type=log_type
            )
            session.add(new_message)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al crear el mensaje de log: {e}")
        finally:
            session.close()
            
    def get_messages_by_slug(self, slug):
        """Obtiene todos los mensajes relacionados con un slug."""
        session = self.SessionLocal()
        try:
            result = session.query(LoggerMessage).filter(LoggerMessage.slug == slug).all()
            return result
        except SQLAlchemyError as e:
            print(f"Error al obtener los mensajes: {e}")
            return []
        finally:
            session.close()
    
    def get_all_request_logs_with_alerts(self):
        """Obtiene todos los registros de RequestLogger con sus respectivos mensajes de LoggerMessage relacionados."""
        session = self.SessionLocal()
        try:
            # Obtener todos los registros de RequestLogger
            request_logs = session.query(RequestLogger).all()
            
            # Crear una lista para almacenar los resultados
            result = []
            
            for log in request_logs:
                # Obtener los mensajes de LoggerMessage relacionados con el slug
                alerts = session.query(LoggerMessage).filter(LoggerMessage.slug == log.slug).all()
                
                # Convertir los mensajes en un formato adecuado (lista de diccionarios)
                alert_messages = [{'log_type': alert.log_type, 'message': alert.message} for alert in alerts]
                
                # Agregar el log y los mensajes al diccionario
                result.append({
                    'slug': log.slug,
                    'request_type': log.request_type,
                    'host': log.host,
                    'request': log.request,
                    'header': log.header,
                    'body': log.body,
                    'created_on': log.created_on.isoformat(),
                    'alert': alert_messages  # Incluir los mensajes relacionados
                })
            
            return result
        
        except SQLAlchemyError as e:
            print(f"Error al obtener los logs con alertas: {e}")
            return []
        finally:
            session.close()
    
    


bridge_local_db = LocalDBBaseConnection()