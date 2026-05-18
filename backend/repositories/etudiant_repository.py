from models.etudiant import Etudiant
from config.database import db


class EtudiantRepository:

    # AUTHENTIFICATION
    @staticmethod
    def get_etudiant_by_matricule_and_password(matricule, password):

        etudiant = Etudiant.query.filter_by(
            matricule=matricule,
            password=password
        ).first()

        return etudiant

    