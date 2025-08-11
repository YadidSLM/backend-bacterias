import pandas as pd
import os
from src.management_db.db import db #Correr desde la terminal en backend-bacterias con python -m src.management_db.load_data
from src.app import app
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path_colombos = os.path.join(base_dir, '..', 'archivos', 'Sente', 'colomboslt2.txt')
file_path_modulo = os.path.join(base_dir, '..', 'archivos', 'Sente', 'SignedCytoscapeInput-nodes-lt2.txt')


colombosBacteria = pd.read_table(file_path_colombos)
nodeModule = pd.read_table(file_path_modulo)

modulo = []
locusTag = []

#Cargar módulos (colores)
for row in nodeModule['nodeAttr[nodesPresent, ]']: #Cargar modulos en una lista sin repetirlos
    if not(row in modulo):
        modulo.append(row)
with app.app_context():
    print("Entro a la app")
    try: #Si no hay registros en la base de datos
        for color in modulo:
            new_modulo = Coexp_modulo(nombre_modulo=color)
            db.session.add(new_modulo)
            db.session.commit()
        else: #Al terminar el for
            print("Datos registrados en la DB")
    except:
         db.session.rollback() #Hace que cancele los session.add y no se suban en el siguiente commit()
         modulo.clear() #Libera espacio al borrar la lista de módulo que ya no se usa
         print("Ya se tienen estos modulos en la BD")



#Cargar genes
for row in colombosBacteria['LocusTag']:
    if not(row in locusTag):
        locusTag.append(row)
with app.app_context():
    print("Entro a la app")
    try:
        for gen in locusTag:
            new_locus_tag = Gen(locus_tag=gen)
            db.session.add(new_locus_tag)
            db.session.commit()
        else:
            print("Datos registrados en la DB")
    except:
         db.session.rollback()
         locusTag.clear()
         print("Ya se tienen estos genes en la BD")

#Cargar expresiones a tabla expresión
print(colombosBacteria.tail(10))

# print(modulo)
# print(locusTag)
# print(len(locusTag))