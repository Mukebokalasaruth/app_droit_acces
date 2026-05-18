from models.surveillant import Surveillant
from config.database import db


class SurveillantRepository:

    # AUTHENTIFICATION
    @staticmethod
    def get_surveillant_by_login_and_password(login, password):

        surveillant = Surveillant.query.filter_by(
            login=login,
            password=password
        ).first()

        return surveillant