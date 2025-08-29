from src.management_db.db import db

class Bacteria(db.Model):
    __tablename__ = 'bacteria'
    id_bacteria = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bacteria = db.Column(db.String(20), unique = True, nullable=False)

    gen = db.relationship('Gen', back_populates='bacteria')

    def __repr__(self): #Para cuando se quiere imprimir el objeto. Es una función que ves su representación.
        return print(f"id_bacteria: {self.id_bacteria}, bacteria: {self.bacteria}")