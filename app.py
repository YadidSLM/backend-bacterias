from flask import Flask
from config import Config
from flask_cors import CORS
from models.db import db

app = Flask(__name__)
app.config.from_object(Config) #Carga atributos de la clase Config como variables de configuración para tu aplicación.

CORS(app)

db.init_app(app) #.init_app(app) es un método de la clase SQLAlchemy para vincular la bd con la aplicación de Flask creada en este archiv que se llama app.


@app.route('/') #Las rutas se implementan con decoradores.
def index():
    return "it works"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000 , debug=True)
    

