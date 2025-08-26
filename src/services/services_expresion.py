from flask import Blueprint, jsonify
from src.models import Expresion, Gen
from src.management_db.db import db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
import io
from flask import request

expresion_app = Blueprint('expresion_app', __name__)

def fig_to_base64(fig, fmt="svg"): #Convierte la gráfica a imagen base64
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    data = buf.getvalue()
    b64 = base64.b64encode(data).decode('ascii')
    mime = "image/svg+xml" if fmt == "svg" else "image/png"
    return f"data:{mime};base64,{b64}"


@expresion_app.route('/boxplot/<locusTag>', methods = ['GET'])
def getLocusExprBoxplot(locusTag):

    gen = db.session.query(Gen).filter(Gen.locus_tag == locusTag).one()
    expr = Expresion.query.filter_by(id_gen = gen.id_gen).all()
    
    expr_list = [ex.expresion for ex in expr] #de cada objeto ex obtiene su atributo expresion

    fig, ax = plt.subplots(figsize=(6,4))
    ax.boxplot(expr_list)
    ax.set_title(gen.locus_tag)
    ax.set_ylabel("Expresión")
    img_data = fig_to_base64(fig, fmt=request.args.get("format", "svg").lower())

    return jsonify({
        "locus" : locusTag,
        "img" : img_data,
        # "expresiones" : expr.__repr__(),
        "valores_expr" : expr_list

    })