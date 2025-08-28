from flask import Blueprint, jsonify
from src.models import Gen, Nodo, Arista
from src.management_db.db import db
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from flask import request

coexp_network = Blueprint('coexp_network', __name__)

def fig_to_base64(fig, fmt="svg"): #Convierte la gráfica a imagen svg y luego a base64
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    data = buf.getvalue()
    b64 = base64.b64encode(data).decode('ascii')
    mime = "image/svg+xml" if fmt == "svg" else "image/png"
    return f"data:{mime};base64,{b64}"

@coexp_network.route('/get-network/<locusTag>', methods = ['GET'])
def getCoexprNetwork(locusTag):
    #Obtener el módulo del locus tag ingresado en la url
    node = db.session.query(Nodo).join(Gen).filter(Gen.locus_tag == locusTag).one_or_none()
    #Obtener la arista cuyo fromNode tenga el locus ingresado.
    idnodo = node.id_nodo
    # aristasRaw = db.session.query(Arista).filter(Arista.id_arista == idnodo).one_or_none()
    suColor = node.modulo.nombre_modulo
    suLocus = node.gen.locus_tag
    aristasRaw = node.arista_from #Lista de asristas que tiene el nodo
    # aristasRaw = node.arista_from[0].from_node.modulo.nombre_modulo #Regresa el módulo del fromNode de esa arista
    """
    Hacer lista de tuplas de todos los nodos (su locus tag porque se puede acceder al id_nodo o id_modulo) en la arista con su respectivo módulo que no haya nodos repetidos. Done
    Hacer lista de tuplas de (locusFrom, locusTo, peso) Done
    *** Después ir a load_data y validar que no se ingresen a la BD aristas que no tengan nodos en cyto_nodes.txt
    """
    node_with_color_list = []
    arista_FNTNW_list = []
    node_with_color_list.append((suLocus, suColor)) #Ingresa el locus tag y módulo de locus buscado
    for arista in aristasRaw:
        nodeLocus = arista.to_node.gen.locus_tag
        nodeModule = arista.to_node.modulo.nombre_modulo
        nodo_and_module = (nodeLocus, nodeModule)
        node_with_color_list.append(nodo_and_module)

        locusFrom = arista.from_node.gen.locus_tag
        locusTo = arista.to_node.gen.locus_tag
        peso = arista.weight
        edge = (locusFrom, locusTo, peso)
        arista_FNTNW_list.append(edge)

    G = nx.Graph()
    nx_node_color = []
    for nod, col in node_with_color_list:
        nx_node_color.append((nod, {"color" : col})) #Se alade una tupla con la segunda localidad un diccionario porque así lo lee networkinx
    G.add_nodes_from(nx_node_color)
    G.add_weighted_edges_from(arista_FNTNW_list)

    colores = []
    for _, dicciColorlor in G.nodes(data=True):
        colores.append(dicciColorlor["color"])
    pesos = []
    for _,_,dicciAristasNx in G.edges(data=True): #G.edges(data=True) coloca el atributo weight en un diccionario.
        pesos.append(dicciAristasNx["weight"] * 10)
    
    nodePositions = nx.spring_layout(G, seed=42, k=0.8)

    fig, ax = plt.subplots(figsize=(10,8))
    nx.draw_networkx_nodes(G, nodePositions, node_color=colores, node_size=1500, ax=ax)
    nx.draw_networkx_edges(G, nodePositions, width=pesos, edge_color="gray", ax = ax)
    nx.draw_networkx_labels(G, nodePositions, font_size=7, font_color="black", font_weight="bold", horizontalalignment="center", verticalalignment="center", ax = ax)
    ax.axis("off")
    
    #Red de coexpresión

    img_data = fig_to_base64(fig, fmt=request.args.get("format", "svg").lower())

    return jsonify({
        "locus" : locusTag,
        "img" : img_data,
        "Nodo" : f"{idnodo}, {suLocus}, {suColor}",
        "Tipo Arista" : f"{type(aristasRaw)}",
        "Arista" : f"{aristasRaw}",
        "Lista de nodos" : f"{node_with_color_list}",
        "Lista aristas" : f"{arista_FNTNW_list}"
    })