from src.management_db.db import db

class Expresion(db.Model):
    __tablename__ = 'expresion'

    id_gen = db.Column(db.Integer, db.ForeignKey('gen.id_gen'), primary_key=True)
    id_muestra = db.Column(db.Integer, nullable=False, primary_key=True) #Este valor podría estar ligado al id de la tabla Muestra, en este caso se insertan los valores de las columnas de la tabla colombosBacteria.txt
    #Se colocó como llave priamria para que permitiera introcudir más de un valor de id_gen para cada muestra, además, si se añaden todas las tablas sería una llave foránea de Muestra
    expresion = db.Column(db.Float, nullable=False) 

    gen = db.relationship('Gen', back_populates='expresiones')

    def __repr__(self):
        return f"<Expresion id_gen = {self.id_gen}, id_muestra = {self.id_muestra}, expresion_valor = {self.expresion}>\n"