from config.database import db

class Comptable(db.Model):
    __tablename__ = 'comptable'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    login = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)