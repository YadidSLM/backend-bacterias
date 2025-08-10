from src.management_db.db import db

class Coexp_modulo(db.Model):
    __tablename__ = 'coexp_modulo'
    
    id_coexp_modulo = db.Column(db.Integer, primary_key=True)
    nombre_modulo = db.Column(db.String(30), unique=True, nullable=False) #Un color es el que representa el módulo

    nodo = db.relationship('Nodo', back_populates='modulo')


    def __repr__(self):
        return f"id_coexp_modulo: {self.id_coexp_modulo} nombre_modulo: {self.nombre_modulo}"