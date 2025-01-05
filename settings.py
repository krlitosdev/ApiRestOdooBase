from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    debug: bool
    dev_url_odoo: str
    dev_db_odoo: str
    dev_user_odoo: str
    dev_password_odoo: str
    prod_url_odoo: str
    prod_db_odoo: str
    prod_user_odoo: str
    prod_password_odoo: str    
    dev_host_sqlserver: str
    dev_port_sqlserver: int
    dev_db_sqlserver: str
    dev_user_sqlserver: str
    dev_password_sqlserver: str    
    prod_host_sqlserver: str
    prod_port_sqlserver: int
    prod_db_sqlserver: str
    prod_user_sqlserver: str
    prod_password_sqlserver: str
    
    model_config = SettingsConfigDict(env_file=".env")

# Importamos las configuraciones de Bases de datos y accesos extras
settings = Settings()