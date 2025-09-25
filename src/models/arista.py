from src.management_db.db import db

class Arista(db.Model):
    __tablename__ = 'arista'

    id_arista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_from_node = db.Column(db.Integer, db.ForeignKey('nodo.id_nodo'), nullable=False)
    id_to_node = db.Column(db.Integer, db.ForeignKey('nodo.id_nodo'), nullable=False)
    weight = db.Column(db.Float)
    # Define una restricción única para evitar duplicados exactos, pero permite múltiples aristas del mismo fromNode y toNode, pero con diferentes pesos
    __table_args__ = (
        db.UniqueConstraint('id_from_node', 'id_to_node', 'weight', name='uq_arista_from_to_weight'),
    )

    #El atributo de la clase Arista es from_node que permite acceder a from_node de la tabla Nodo. En objetos python
    from_node = db.relationship('Nodo', foreign_keys=[id_from_node], back_populates='arista_from')
    to_node = db.relationship('Nodo', foreign_keys=[id_to_node], back_populates='arista_to')

    def __repr__(self):
        return f"<Arista id_arista = {self.id_arista}>, id_from_node = {self.id_from_node}, id_to_node = {self.id_to_node}, weight = {self.weight}"

