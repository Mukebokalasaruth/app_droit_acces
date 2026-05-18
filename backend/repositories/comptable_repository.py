from models.comptable import Comptable
from config.database import db


class ComptableRepository:

    # AUTHENTIFICATION
    @staticmethod
    def get_comptable_by_login_and_password(login, password):

        comptable = Comptable.query.filter_by(
            login=login,
            password=password
        ).first()

        return comptable