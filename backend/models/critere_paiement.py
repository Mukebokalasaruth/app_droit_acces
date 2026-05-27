from config.database import db

class CriterePaiement(db.Model):
    __tablename__ = 'criterePaiement'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    montant = db.Column(db.Float, nullable=False)

    session = db.Column(db.String(50), nullable=False)

    idPromotion = db.Column(
        db.Integer,
        db.ForeignKey('promotion.id'),
        nullable=False
    )