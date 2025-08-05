from src.app import app
from src.management_db.db import db
#Modelos de las tablas a crear.
from src.models.usuario import Usuario

with app.app_context():
    db.create_all()
    print("Database created.")