from src.app import app
from src.management_db.db import db
#Modelos de las tablas a crear.
# from src.models.modelos import Gene, Condition, Sample, Expression, CoexpressionModule, TranscriptionFactor, GeneTF, Node, Edge
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion

#Aquí importar los datos de las 3 tablas que ocupan los datos para la bd.

with app.app_context():
    db.create_all()
    print("Database created.")