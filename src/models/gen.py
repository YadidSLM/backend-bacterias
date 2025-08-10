from src.management_db.db import db

class Gen(db.Model):
    __tablename__ = 'gen'
    id_gen = db.Column(db.Integer, primary_key=True)
    locus_tag = db.Column(db.String(20), unique = True, nullable=False)

    nodo = db.relationship('Nodo', back_populates='gen')
    expresiones = db.relationship('Expresion', back_populates='gen')

    def __repr__(self): #Para cuando se quiere imprimir el objeto. Es una función que ves su representación.
        return print(f"id_gen: {self.id} \nlocus_tag: {self.locus_tag}")
