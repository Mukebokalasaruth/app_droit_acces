from models.preuve_paiement import PreuvePaiement
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
    # CONSULTER ETAT VALIDATION
    # ==========================
    @staticmethod
    def consulter_etat_validation(
        id_etudiant
    ):

        preuve = (
            PreuvePaiement.query
            .filter_by(
                idEtudiant=id_etudiant
            )
            .order_by(
                PreuvePaiement.id.desc()
            )
            .first()
        )

        return preuve

    