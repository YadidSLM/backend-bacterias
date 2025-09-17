import pandas as pd
import os
from src.management_db.db import db #Corre desde la terminal en backend-bacterias con python -m src.management_db.load_data
from src.app import app
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion, Bacteria

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path_colombos = os.path.join(base_dir, '..', 'archivos', 'Ypest', 'colombosypest.txt')
file_path_modulo = os.path.join(base_dir, '..', 'archivos', 'Ypest', 'SignedCytoscapeInput-nodes-ypest-Bicor00.txt')
file_path_aristas = os.path.join(base_dir, '..', 'archivos', 'Ypest', 'Signed-CytoscapeInput-edges-ypest-Bicor00.txt')
#Signed-CytoscapeInput-edges-lt2.txt


colombosBacteria = pd.read_table(file_path_colombos)
nodeModule = pd.read_table(file_path_modulo)
aristasDataFrame = pd.read_table(file_path_aristas)

modulo = []
locusTag = []
expresion = []
nodosList =[]
#Cargar bacterias
"""
id_bacteria  bacteria
1   Ypest
2   Tther
3   Spneu
4   Smeli   Para cargar archivos de otras bacterias, cambiar el nombre de los archivos colombos, nodes y edges a los de la bacteria que se quiera cargar.
5   Sflex   Y cambiar bacterias[0] en la línea 89 por el índice de la bacteria que se quiera cargar, por ejemplo, para Mtube es bacterias[7], ojo que el índice es 7 aunque el id_bacteria es 6.
6   Sente
7   Paeru
8   Mtube
9   Lrham
10  Hpylo
11  Ecoli
12  CjejuB).j
13  Cacet
14  Bthet
15  Bsubt
16  Bcere
17  Banth
"""
bacterias = ["Ypest", "Tther", "Spneu", "Smeli", "Sflex", "Sente", "Paeru", "Mtube", "Lrham", "Hpylo", "Ecoli", "Cjeju", "Cacet", "Bthet", "Bsubt", "Bcere", "Banth"]#Lista de bacterias
with app.app_context():
    print("Entro a la app bacterias")
    try: #Si no hay registros en la base de datos
        for bacteria in bacterias:
            new_bacteria = Bacteria(bacteria=bacteria)
            db.session.add(new_bacteria)
            db.session.commit()
        else: #Al terminar el for
            print("Bacterias registradas en la DB")
    except:
         db.session.rollback() #Hace que cancele los session.add y no se suban en el siguiente commit()
         print("Ya se tienen estas bacterias en la BD")
    

print(nodeModule.columns)
#Cargar módulos (colores)
for row in nodeModule['nodeAttr[nodesPresent, ]']: #Cargar modulos en una lista sin repetirlos
    if not(row in modulo):
        modulo.append(row)
with app.app_context():
    print("Entro a la app módulos")
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

#.itertuplas


#Cargar genes
for row in colombosBacteria['LocusTag']:
    if not(row in locusTag): #Asegura que no hay valores repetidos de locus tag
        locusTag.append(row)
with app.app_context():
    print("Entro a la app genes")
    #bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacteria[0]).one_or_none() #Por ahora todos son de Ypest, id_bacteria=1, bacterias[0] es Ypest
    bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacterias[0]).one_or_none() #Por ahora todos son de Ypest, id_bacteria=1, bacterias[0] es Ypest
    print(f"bacteria: {bact.bacteria}, id_bacteria: {bact.id_bacteria}")
    try:
        if bact:
            for gen in locusTag:
                new_locus_tag = Gen(locus_tag=gen, id_bacteria=bact.id_bacteria) #Se obtiene el id_bacteria de la consulta anterior
                db.session.add(new_locus_tag)
                db.session.commit()
            else:
                print("Genes registrados en la DB")
        else:
            print("No se encontró la bacteria")
    except Exception as e:
        db.session.rollback()
        locusTag.clear()
        print("Ya etsán los datos en la BD o Error al insertar genes:", str(e))
    #raise SystemExit #Sale del programa si ya están los genes, pues las demás tablas dependen de estos.
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

El tipo de dato float sí acepta valores NaN como registros, los int no,
Se saca cada fila de locus con sus muestras, se convierte a una lista,
luego se itera en cada valor de la lista para tener las expresiones una por una,
una vez que termiana la última muestra del locus, con el for que itera sobre todos los
genes, cambia al que sigue y vuelve a hacer lo mismo, tarda en ejecutarse, pues
su complejidad es n^2.
"""

with app.app_context():
    print("Entro a la app expresion")
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
                    if pd.isna(expr):
                        print(expr)
                        expr = 0
                    new_expresion = Expresion(id_gen=id_locus_tag, id_muestra=id_sample, expresion=expr)
                    db.session.add(new_expresion)
                    db.session.commit()
    except:
        db.session.rollback()
        all_LocusTags.clear()
        print("Ya se tienen las expresiones de colombos.txt en la BD")

#Cargar nodos
"""
Busca en la tabla cada nodeName con su respectivo módulo, pasa los datos de dataFrame a una lista de tuplas,
descompone las tuplas en nodeName y module y obtiene su id_gen e id_módulo de la base de datos para verificar
que ya se hayan ingresado esos genes y módulos y para obtener sus ids que se ingresan en la tabla nodo, luego
inserta el id_gen en la columna de la tabla Nodo con su respectivo id_modulo, id_nodo se autoincrementa.
En caso de que haya en la tabla .txt más nodos que no estén en colombos, guardarlos en una lista y
pregntar a Edgardo qué hacer con esos. No fue el caso.
"""
nodosDataFrame = nodeModule.loc[0:, ["nodeName", "nodeAttr[nodesPresent, ]"]]
nodosList = nodosDataFrame.values.tolist() #Lista de tuplas
with app.app_context():
    print("Entró en la app nodos")
    try:
        for row in nodosList:
            nodeName, module = row
            gen = db.session.query(Gen).filter(Gen.locus_tag == nodeName).one_or_none() #Saca el gen que tiene módulo, esos genes que tienen módulo son nodeName que se obtiene de la tabla.
            moduleColor = db.session.query(Coexp_modulo).filter(Coexp_modulo.nombre_modulo == module).one_or_none()
            #Nodos
            # print(f"id_gen: {gen.locus_tag}, id_coexp_modulo: {moduleColor.nombre_modulo}")
            if(gen and moduleColor):
                print(f"id_gen: {gen.id_gen}, id_coexp_modulo: {moduleColor.id_coexp_modulo}")
                new_nodo = Nodo(id_gen = gen.id_gen, id_coexp_modulo = moduleColor.id_coexp_modulo)
                db.session.add(new_nodo)
                db.session.commit()
            else:
                print("No se obtuvieron datos requeridos")
                break
        else:
            print("Nodos registrados en la BD")
    except:
        db.session.rollback()
        print("Ya se tienen estos nodos de nodes.txt en la BD")

dfArista_FN_TN_W = aristasDataFrame.loc[0:, ["fromNode", "toNode", "weight"]] #df es dataframe
edges_not_in_nodes = []
with app.app_context():
    print("Entró en la app aristas")
    try:
        for row in dfArista_FN_TN_W.itertuples(index = False, name = None):
            fromNode, toNode, peso = row
            fromNode_value = db.session.query(Nodo).join(Gen).filter(Gen.locus_tag == fromNode).one_or_none()
            toNode_value = db.session.query(Nodo).join(Gen).filter(Gen.locus_tag == toNode).one_or_none()
            if fromNode_value and toNode_value:
                new_arista = Arista(id_from_node = fromNode_value.id_nodo, id_to_node = toNode_value.id_nodo, weight = peso) #fromNode_value es un objeto de modelado en models que tiene como atributo columnas y una de ellas es id_node
                db.session.add(new_arista)
                db.session.commit()
                print(f"{fromNode_value.id_gen}: {fromNode}, {toNode_value.id_gen}: {toNode}, weight: {peso}")
            else:
                #Estos genes tienen baja correlación, por eso no están en nodos.
                edges_not_in_nodes.append((fromNode, toNode, peso))
                print(f"No se encuentran los locus_tag de la tabla edges.txt: fromNode: {fromNode}, toNode: {toNode} en la BD")
    
    except Exception as e:
        db.session.rollback()
        print("Ya están los datos en la BD o Error al insertar aristas:", str(e)) #El error es que no había nodos (de dfArista_FN_TN_W) en la BD nodo (y tampoco están en cyto..nodes.txt pues de esa tabla se llenó la tabla nodo), para que no cayera en el error se cambió de one() a one_or_none() para saber qué aristas intenta hacer la relación de la tabla edges.txt, pero no puede porque no están en nodos.
        
        # print("Ya se tienen registrados las aristas en la BD.")
#Para Ypest, no hay nodos de las aristas que no estén en nodos, SMELI es una bacteria que le faltan datos en sus tablas.
print(edges_not_in_nodes) #Estaba viendo las tablas y veo que sí se contempla una relación entre esos genes con un peso, pero no están en la de nodos con su módulo, ¿es cierto que no se incluyen en nodos aquellos genes que no tienen una relación tan fuerte?
    
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