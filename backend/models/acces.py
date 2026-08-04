from config.database import db

class Acces(db.Model):
    __tablename__ = 'acces'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    matriculeEtudiant = db.Column(db.String(50), nullable=False)