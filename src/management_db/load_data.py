import pandas as pd
import os
from src.management_db.db import db #Corre este script desde la terminal en backend-bacterias con python -m src.management_db.load_data como se indica en README.md
from src.app import app
from src.models import Gen, Nodo, Arista, Coexp_modulo, Expresion, Bacteria

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path_colombos = os.path.join(base_dir, '..', 'archivos', 'Ecoli', 'colombosEcoli.txt')
file_path_modulo = os.path.join(base_dir, '..', 'archivos', 'Ecoli', 'SignedCytoscapeInput-nodes-Ecoli-Bicor140.txt')
file_path_aristas = os.path.join(base_dir, '..', 'archivos', 'Ecoli', 'Signed-CytoscapeInput-edges-Ecoli-Bicor140.txt')
#Signed-CytoscapeInput-edges-lt2.txt


colombosBacteria = pd.read_table(file_path_colombos)
nodeModule = pd.read_table(file_path_modulo)
aristasDataFrame = pd.read_table(file_path_aristas)

modulo = []
locusTag = []
expresion = []
nodosList =[]

print("Columnas de nodeModule:", nodeModule.columns)

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
bacterias = ["Ypest", "Tther", "Spneu", "Smeli", "Sflex", "Sente", "Paeru", "Mtube", "Lrham", "Hpylo", "Ecoli", "Cjeju", "Cacet", "Bthet", "Bsubt", "Bcere", "Banth"]#Lista de bacterias, el índice de esta lista es el id_bacteria - 1
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
            existente = db.session.query(Coexp_modulo).filter_by(nombre_modulo=color).one_or_none()
            if not existente:
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
indiceBacteria = 10 #Índice de la bacteria que se quiere cargar, por ejemplo, para Mtube es 7, ojo que el índice es 7 aunque el id_bacteria es 8.
for row in colombosBacteria['LocusTag']:
    if not(row in locusTag): #Asegura que no hay valores repetidos de locus tag
        locusTag.append(row)
with app.app_context():
    print("Entro a la app genes")
    bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacterias[indiceBacteria]).one_or_none() #Insertar el índice de la bacteria que se quiera cargar aquí, por ejemplo, para Mtube es bacterias[7], ojo que el índice es 7 aunque el id_bacteria es 8.
    print(f"bacteria: {bact.bacteria}, id_bacteria: {bact.id_bacteria}")

    try:
        if bact:
            for gen in locusTag:
                new_locus_tag = Gen(locus_tag=gen, id_bacteria=bact.id_bacteria) #Se obtiene el id_bacteria de la consulta anterior
                existente = db.session.query(Gen).filter_by(locus_tag=gen, id_bacteria=bact.id_bacteria).one_or_none()
                if not existente:
                    print("Se ingresa nuevo gen")
                    db.session.add(new_locus_tag)
                    db.session.commit()
                else:
                    #print(f"Ya existe el gen (locus_tag): {gen} en la base de datos")
                    continue
                
            else:
                print("Genes registrados en la DB")
        else:
            print("No se encontró la bacteria")
    except Exception as e:
        db.session.rollback()
        locusTag.clear()
        print("Ya etsán los datos en la BD o Error al insertar genes:", str(e))

#Cargar expresiones
with app.app_context():
    print("Entro a la app expresion")
    try:
        bact = db.session.query(Bacteria).filter(Bacteria.bacteria == bacterias[indiceBacteria]).one_or_none() #Insertar el índice de la bacteria que se quiera cargar aquí, por ejemplo, para Mtube es bacterias[7], ojo que el índice es 7 aunque el id_bacteria es 8.
        all_LocusTags = db.session.query(Gen).filter(Gen.id_bacteria == bact.id_bacteria).all() #Hay que hacer restricción para que sólo saque los locus_tag de la bacteria que se está cargando, por ejemplo, para Mtube es id_bacteria=8
        # Ej. locus_tag = 'PSLT099'
        all_LocusTags = [(gen.id_gen, gen.locus_tag) for gen in all_LocusTags] #Lista de tuplas (id_gen, locus_tag)
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
    except Exception as e:
        db.session.rollback()
        all_LocusTags.clear()
        print("Ya se tienen las expresiones de colombos.txt en la BD, o Error al insertar expresiones:", str(e))

#Cargar nodos
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
                print(f"No se obtuvieron datos requeridos {nodeName}, {module}")
                break
        else:
            print("Nodos registrados en la BD")
    except:
        db.session.rollback()
        print("Ya se tienen estos nodos de nodes.txt en la BD")

#Cargar aristas
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
                existente = db.session.query(Arista).filter_by(id_from_node=fromNode_value.id_nodo, id_to_node=toNode_value.id_nodo, weight=peso).one_or_none()
                if not existente:
                    new_arista = Arista(id_from_node = fromNode_value.id_nodo, id_to_node = toNode_value.id_nodo, weight = peso) #fromNode_value es un objeto de modelado en models que tiene como atributo columnas y una de ellas es id_node
                    db.session.add(new_arista)
                    db.session.commit()
                    print(f"Registrando {fromNode_value.id_gen}: {fromNode}, {toNode_value.id_gen}: {toNode}, weight: {peso}")
                else:
                    print(f"Ya existe la arista: fromNode: {fromNode}, toNode: {toNode}, weight: {peso}")
                    exit()
            else:
                #Estos genes tienen baja correlación, por eso no están en nodos.
                edges_not_in_nodes.append((fromNode, toNode, peso))
                print(f"No se encuentran los locus_tag de la tabla edges.txt: fromNode: {fromNode}, toNode: {toNode} en la BD")
                #print(nodeModule.head(10))
                print(nodeModule[nodeModule['nodeName'] == "plum2"]) #Muestra si los locus_tag de las aristas que no se encuentran en la BD están en nodes.txt
                exit()
                
    
    except Exception as e:
        db.session.rollback()
        print("Ya están los datos en la BD o Error al insertar aristas:", str(e)) #El error es que no había nodos (de dfArista_FN_TN_W) en la BD nodo (y tampoco están en cyto..nodes.txt pues de esa tabla se llenó la tabla nodo), para que no cayera en el error se cambió de one() a one_or_none() para saber qué aristas intenta hacer la relación de la tabla edges.txt, pero no puede porque no están en nodos.

#Para Ypest, no hay nodos de las aristas que no estén en nodos (están completas las tablas .txt). SMELI es una bacteria que le faltan datos en sus tablas.
print(edges_not_in_nodes) #Lista de tuplas (fromNode, toNode, weight) que no se encuentran en nodos. Se incluye esta lista por si le faltan datos a la tabla nodes.txt (como en el caso de SMELI) y se quieren agregar esos nodos faltantes a la tabla nodo de la BD.