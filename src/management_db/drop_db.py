from src.app import app
from src.management_db.db import db
#Modelos de las tablas que se borran.
# from src.models.modelos import Gene, Condition, Sample, Expression, CoexpressionModule, TranscriptionFactor, GeneTF, Node, Edge
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion

with app.app_context():
    db.drop_all()
    print("Tablas borradas.")