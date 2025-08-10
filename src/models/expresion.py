from src.management_db.db import db

class Expresion(db.Model):
    __tablename__ = 'expreesion'

    id_gen = db.Column(db.Integer, db.ForeignKey('gen.id_gen'), primary_key=True)
    id_muestra = db.Column(db.Integer, unique=True, nullable=False) #Este valor puede estar ligado al id de l atabla Muestra, en este caso se insertan los valores de las columnas de la tabla colombosBacteria.txt
    expresion = db.Column(db.Integer, nullable=False)

    gen = db.relationship('Gen', back_populates='expresiones')

    def __repr__(self):
        return f"id_expresion: {self.id_expresion}, id_muestra: {self.id_muestra}, expresion_valor: {self.expresion}"