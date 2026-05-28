from models.etudiant import Etudiant
from models.surveillant import Surveillant
from config.database import db
from models.preuve_paiement import PreuvePaiement


class SurveillantRepository:

    # AUTHENTIFICATION
    @staticmethod
    def get_surveillant_by_login_and_password(login, password):

        surveillant = Surveillant.query.filter_by(
            login=login,
            password=password
        ).first()

        return surveillant
    

    # RECHERCHER ETUDIANT

    @staticmethod
    def get_etudiant_by_matricule(
        matricule
    ):

        etudiant = (
            Etudiant.query
            .filter_by(
                matricule=matricule
            )
            .first()
        )

        return etudiant
    
    # DERNIERE PREUVE PAIEMENT
    
    @staticmethod
    def get_last_preuve(
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

    # ETUDIANTS VALIDES PAR PROMO
    
    @staticmethod
    def get_etudiants_valides_by_promotion(
        id_promotion
    ):

        result = (
            Etudiant.query
            .join(
                PreuvePaiement,
                Etudiant.id ==
                PreuvePaiement.idEtudiant
            )
            .filter(
                Etudiant.idPromotion
                == id_promotion,

                PreuvePaiement
                .statutValidation
                == True
            )
            .all()
        )

        return result
    