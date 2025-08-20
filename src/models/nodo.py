from src.management_db.db import db

class Nodo(db.Model):
    __tablename__ = 'nodo'

    id_nodo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_gen = db.Column(db.Integer, db.ForeignKey('gen.id_gen'), nullable=False)
    id_coexp_modulo = db.Column(db.Integer, db.ForeignKey('coexp_modulo.id_coexp_modulo'), nullable="False")

    __table_args__ = (
        db.UniqueConstraint('id_gen', 'id_coexp_modulo', name = 'unico_gen_modulo'),
    )

    gen = db.relationship('Gen', back_populates='nodo')
    modulo = db.relationship('Coexp_modulo', back_populates='nodo')
    arista_from = db.relationship('Arista', foreign_keys='Arista.id_from_node', back_populates='from_node') #El atributo de la clase Nodo es arista y con ella se puede accede a la arista que contiene el nodo.
    arista_to = db.relationship('Arista', foreign_keys='Arista.id_to_node', back_populates='to_node')

    def __repr__(self):
        return f"id_nodo: {self.id_nodo}, id_gen: {self.id_gen}, id_coexp_modulo: {self.id_coexp_modulo}"