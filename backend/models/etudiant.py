from config.database import db

class Etudiant(db.Model):
    __tablename__ = 'etudiant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(255), nullable=False)
    postnom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    matricule = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    idPromotion = db.Column(db.Integer, db.ForeignKey('promotion.id'), nullable=False)