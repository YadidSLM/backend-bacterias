from src.app import app
from src.management_db.db import db
#Modelos de las tablas a crear.
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion

#Aquí importar los datos de las 3 tablas que ocupan los datos para la bd.
"""
Los modelos definen las tablas con el objeto db de SQLAlchemy y en create_db.py se tiene:
with app.app_context(): # with (una estructra de control que maneja contextos) permite que Flask-SQLAlchemy acceda a la configuración (URI de conexión)
    db.create_all() # Crea las tablas gracias a lo definido en db en models.py y sabe dónde crearlas por el with de arriba.

"""
with app.app_context():
    db.create_all()
    print("Database created.")