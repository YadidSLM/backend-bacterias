from flask import Flask
from src.config import Config
from flask_cors import CORS
from src.management_db.db import db

from src.services.services_expresion import expresion_app
from src.services.services_coexp_network import coexp_network

app = Flask(__name__)
app.config.from_object(Config) #Carga atributos de la clase Config como variables de configuración para tu aplicación. Le dice a la app cómo conectarse con postgres.

CORS(app)

db.init_app(app) #.init_app(app) es un método de la clase SQLAlchemy para vincular la bd con la aplicación de Flask creada en este archivo que se llama app. Conecta la app Flask con el objeto db del tipo: SQLAlchemy

"""
Los modelos definen las tablas con el objeto db de SQLAlchemy y en create_db.py se tiene:
with app.app_context(): # with (una estructra de control que maneja contextos) permite que Flask-SQLAlchemy acceda a la configuración (URI de conexión)
    db.create_all() # Crea las tablas gracias a lo definido en db en models.py y sabe dónde crearlas por el with de arriba.

"""

app.register_blueprint(expresion_app, url_prefix = '/expresion')
app.register_blueprint(coexp_network, url_prefix = '/coexpresion_network')


@app.route('/') #Las rutas se implementan con decoradores.
def index():
    return "it works"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000 , debug=True)
    

