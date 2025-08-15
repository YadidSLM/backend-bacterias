import pandas as pd
import os
from src.management_db.db import db #Corre desde la terminal en backend-bacterias con python -m src.management_db.load_data
from src.app import app
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path_colombos = os.path.join(base_dir, '..', 'archivos', 'Sente', 'colomboslt2.txt')
file_path_modulo = os.path.join(base_dir, '..', 'archivos', 'Sente', 'SignedCytoscapeInput-nodes-lt2.txt')


colombosBacteria = pd.read_table(file_path_colombos)
nodeModule = pd.read_table(file_path_modulo)

modulo = []
locusTag = []
expresion = []

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
            print("Módulos registrados en la DB")
    except:
         db.session.rollback() #Hace que cancele los session.add y no se suban en el siguiente commit()
         modulo.clear() #Libera espacio al borrar la lista de módulo que ya no se usa
         print("Ya se tienen estos modulos en la BD")



#Cargar genes
for row in colombosBacteria['LocusTag']:
    if not(row in locusTag): #Asegura que no hay valores repetidos de locus tag
        locusTag.append(row)
with app.app_context():
    print("Entro a la app")
    try:
        for gen in locusTag:
            new_locus_tag = Gen(locus_tag=gen)
            db.session.add(new_locus_tag)
            db.session.commit()
        else:
            print("Genes registrados en la DB")
    except:
         db.session.rollback()
         locusTag.clear()
         print("Ya se tienen estos genes en la BD")

#Cargar expresiones a tabla expresión
# print(colombosBacteria['2'].head(10))
# for row in colombosBacteria['LocusTag']:
#     print(f"{row}")
"""
Obtener los id_locus_tag de la base de datos, ponerlos en una
lista para iterar la lista y con la variable que itere la lista
index ponerla en colombosBacteria.loc[index], lugeo filtrar
valores nulos e indicar cuáles son para saber si cambiarlos a cero o no
dependiendo si la base de datos permite esos valores NaN y guardar la fila en
otra lista de listas con el primer índice el locus tag y su contenido
cada una de las muestras (fila extraida), por último iterar sobre ca
"""
print(type(colombosBacteria.loc[0]))

with app.app_context():
    print("Entro a la app")
    try:
        all_LocusTags = db.session.query(Gen.id_gen, Gen.locus_tag).all()
        # locus_tag = 'PSLT099'
        for id_locus_tag, locus_tag in all_LocusTags:
            print(f"{id_locus_tag}, {locus_tag}")
            locus_expr_dataFrame = colombosBacteria[colombosBacteria['LocusTag'].str.contains(locus_tag)] #Regresa la fila que se indica en contains .
            locus_expr_values = locus_expr_dataFrame.values.tolist()
            # print(colombosBacteria.loc[0].isna().sum()) #Regresa  el número de valores nan de la fila con índice 0.
            for id_sample, expr in enumerate(locus_expr_values[0]): #La primera localidad tiene todos lo resultados por eso locus_expr_values[0]
                if type(expr) is str:
                    print(f"{id_sample}, {expr}") #Este es el locus tag en cadena, por eso se aparta este valor y no se ingresa en la base de datos.            
                else:
                    new_expresion = Expresion(id_gen=id_locus_tag, id_muestra=id_sample, expresion=expr)
                    db.session.add(new_expresion)
                    db.session.commit()
    except:
        db.session.rollback()
        locusTag.clear()
        print("Ya se tienen las expresiones de colombos.txt en la BD")
# locus_tag = 'PSLT099'
# # all_locus_expr = colombosBacteria.loc[colombosBacteria['LocusTag'] == id_locus_tag]
# locus_expr = colombosBacteria[colombosBacteria['LocusTag'].str.contains(locus_tag)] #Regresa la columna que tiene el contains 
# print(locus_expr.values.tolist())
# for expre in locus_expr:
# print(all_locus_expr.loc[id_locus_tag])
    # print(expre)
# print(type(locus_expr))

# for id_muestra, val in enumerate(colombosBacteria.loc[colombosBacteria['LocusTag'] == id_locus_tag]): #.loc[0] devuelve la primera fila de la tabla y el for itera sobre cada valor de la fila.
#     if type(val) is str:
#         print(f"{id_muestra} : {val}") #Este es el locus tag
        
#     else:
#         print(f"{id_locus_tag} : {id_muestra} : {float(val)}")

# print(modulo)
# print(locusTag)
# print(len(locusTag))