"""
---------------------------------    Para continuar el proyecto  ---------------------------------
Este es el archivo de python generado por ChatGPT-4 que genera las tablas en la base de datos
de todas las relaciones (normalizadas hasta la 3ra forma normal por ChatGPT-4) que se encuentran
en los 5 archivos de cada bacteria que están en el drive.

En el proyecto solo ocupó e instanció en la base de datos 3 de estas tablas para desplegar
específicamente el boxplot y la red de coexpresión; sin embargo, en este archivo se añaden todas las relaciones
que genera la base de datos por si se desea trabajar con esos datos que también están disponibles.
Diagrama entidad - relación explicado disponible los documentos del proyecto.

Esos datos son:
-   Genes que están relacionados a un factor de transcripción. (Se puede usar para cambiar la forma de los nodos en la red de coexpresión indicando si es un factor de transcripción)
-   Tabla que describe los factores de transcripción. (Para dar información del TF)
-   Tabla que describe cada muestra, incluyendo la condición experminetal y de referencia de la muestra. (Por si se quiere saber las condicones de cada muestra)

Para llenar los registros en esta base de datos, es necesario hacer el archivo que lea los datos de los archivos .txt
del drive y los pase a la base de datos, se suguiere hacerlo con el ORM SQLAchemy para que en un solo módulo python se lea
el .txt y se inserten los valores en la base de datos.

"""
from src.management_db.db import db

class Gene(db.Model):
    __tablename__ = 'gene'
    gene_id = db.Column(db.Integer, primary_key=True)
    locus_tag = db.Column(db.String, unique=True, nullable=False)

    expressions = db.relationship('Expression', back_populates='gene')
    tf_links = db.relationship('GeneTF', back_populates='gene')
    node = db.relationship('Node', back_populates='gene', uselist=False)


class TranscriptionFactor(db.Model):
    __tablename__ = 'transcription_factor'
    tf_id = db.Column(db.Integer, primary_key=True)
    hmm_acc = db.Column(db.String, nullable=False)
    hmm_name = db.Column(db.String, nullable=False)
    seq_id = db.Column(db.String, nullable=False)

    gene_links = db.relationship('GeneTF', back_populates='tf')


class GeneTF(db.Model):
    __tablename__ = 'gene_tf'
    gene_id = db.Column(db.Integer, db.ForeignKey('gene.gene_id'), primary_key=True)
    tf_id = db.Column(db.Integer, db.ForeignKey('transcription_factor.tf_id'), primary_key=True)

    gene = db.relationship('Gene', back_populates='tf_links')
    tf = db.relationship('TranscriptionFactor', back_populates='gene_links')


class CoexpressionModule(db.Model):
    __tablename__ = 'coexpression_module'
    module_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String, nullable=False)

    nodes = db.relationship('Node', back_populates='module')


class Node(db.Model):
    __tablename__ = 'node'
    node_id = db.Column(db.Integer, primary_key=True)
    gene_id = db.Column(db.Integer, db.ForeignKey('gene.gene_id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('coexpression_module.module_id'), nullable=False)

    gene = db.relationship('Gene', back_populates='node')
    module = db.relationship('CoexpressionModule', back_populates='nodes')
    edges_from = db.relationship('Edge', foreign_keys='Edge.from_node_id', back_populates='from_node')
    edges_to = db.relationship('Edge', foreign_keys='Edge.to_node_id', back_populates='to_node')


class Edge(db.Model):
    __tablename__ = 'edge'
    edge_id = db.Column(db.Integer, primary_key=True)
    from_node_id = db.Column(db.Integer, db.ForeignKey('node.node_id'), nullable=False)
    to_node_id = db.Column(db.Integer, db.ForeignKey('node.node_id'), nullable=False)
    weight = db.Column(db.Float)
    direction = db.Column(db.String) #Al parecer en todas las tablas 'edge' la fila fromnode tonode es siempre undirected

    from_node = db.relationship('Node', foreign_keys=[from_node_id], back_populates='edges_from')
    to_node = db.relationship('Node', foreign_keys=[to_node_id], back_populates='edges_to')


class Condition(db.Model):
    __tablename__ = 'condition'
    condition_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    experimental_samples = db.relationship('Sample', foreign_keys='Sample.condition_id', back_populates='condition')
    reference_samples = db.relationship('Sample', foreign_keys='Sample.ref_condition_id', back_populates='ref_condition')


class Sample(db.Model):
    __tablename__ = 'sample'
    sample_id = db.Column(db.Integer, primary_key=True)
    sample_code = db.Column(db.String, unique=True, nullable=False)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.condition_id'), nullable=False)
    ref_condition_id = db.Column(db.Integer, db.ForeignKey('condition.condition_id'))
    experiment_id = db.Column(db.String)
    data_source = db.Column(db.String)
    platform = db.Column(db.String)

    condition = db.relationship('Condition', foreign_keys=[condition_id], back_populates='experimental_samples')
    ref_condition = db.relationship('Condition', foreign_keys=[ref_condition_id], back_populates='reference_samples')
    expressions = db.relationship('Expression', back_populates='sample')


class Expression(db.Model):
    __tablename__ = 'expression'
    gene_id = db.Column(db.Integer, db.ForeignKey('gene.gene_id'), primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.sample_id'), primary_key=True)
    expr_value = db.Column(db.Float)

    gene = db.relationship('Gene', back_populates='expressions')
    sample = db.relationship('Sample', back_populates='expressions')
