from datetime import datetime
from config.database import db


class PreuvePaiement(db.Model):

    __tablename__ = 'preuvePaiement'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    cheminCapture = db.Column(
        db.Text,
        nullable=False
    )

    statutValidation = db.Column(
        db.Boolean,
        default=False
    )

    motifRejet = db.Column(
        db.Text,
        nullable=True
    )

    idEtudiant = db.Column(
        db.Integer,
        db.ForeignKey('etudiant.id'),
        nullable=False
    )

    dateSoumission = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

