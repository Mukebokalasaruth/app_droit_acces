from config.database import db

class Surveillant(db.Model):
    __tablename__ = 'surveillant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    login = db.Column(db.String(50), nullable=False)