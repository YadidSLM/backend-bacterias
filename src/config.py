import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()
"""
for key, val in os.environ.items():
    print(f"{key} = {val}")
"""
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:' + os.environ.get('DB_PASSWORD') + '@localhost:5432/bacterias'
    #os.environ.get() es una forma de leer variables de entorno del sistema, os es un módulo estandard de python que sirve para interactuar con el sistema operativo.
    #Busca la variable de entorno 'DATABASE_URL' si no la encuentra construye la URL con la variable de entorno 'DB_PASSWORD' y esto es para no ver la constraseña de la BD en el código.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
