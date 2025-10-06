import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Cargar variables del archivo .env
load_dotenv()

class Config:
    # Escapar la contraseña en caso de caracteres especiales
    DB_PASSWORD = quote_plus(os.environ.get('DB_PASSWORD', ''))
    
    # Construir la URL de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ.get('DB_USER', 'postgres')}:{DB_PASSWORD}"
        f"@{os.environ.get('DB_HOST', 'localhost')}:{os.environ.get('DB_PORT', '5432')}/"
        f"{os.environ.get('DB_NAME', 'bacterias_db')}"
    )

    # Evitar warnings de Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Para ver tablas entrar a postgres desde la terminal con: psql -h localhost -U bacterias_user -d bacterias
    #Ver tablas con: \dt
    #Salir de psql con: \q
    #Describir tabla con: \d nombre_de_la_tabla
    #Para hacer respaldos de la bd: pg_dump -U bacterias_user -h localhost -s -d bacterias > respaldo_bacterias.sql