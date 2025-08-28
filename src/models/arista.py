from src.management_db.db import db

class Arista(db.Model):
    __tablename__ = 'arista'

    id_arista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_from_node = db.Column(db.Integer, db.ForeignKey('nodo.id_nodo'), nullable=False)
    id_to_node = db.Column(db.Integer, db.ForeignKey('nodo.id_nodo'), nullable=False)
    weight = db.Column(db.Float)

    #El atributo de la clase Arista es from_node que permite acceder a from_node de la tabla Nodo. En objetos python
    from_node = db.relationship('Nodo', foreign_keys=[id_from_node], back_populates='arista_from')
    to_node = db.relationship('Nodo', foreign_keys=[id_to_node], back_populates='arista_to')

    def __repr__(self):
        return f"<Arista id_arista = {self.id_arista}>, id_from_node = {self.id_from_node}, id_to_node = {self.id_to_node}, weight = {self.weight}"

