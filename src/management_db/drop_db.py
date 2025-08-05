from src.app import app
from src.management_db.db import db
#Modelos de las tablas que se borran.
from src.models.usuario import Usuario

with app.app_context():
    db.drop_all()
    print("Tablas borradas.")