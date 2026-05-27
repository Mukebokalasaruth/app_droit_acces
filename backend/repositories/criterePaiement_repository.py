from models.critere_paiement import CriterePaiement
from config.database import db


class CriterePaiementRepository:

    @staticmethod
    def create(montant, session, id_promotion):
        critere = CriterePaiement(
            montant=montant,
            session=session,
            idPromotion=id_promotion
        )

        db.session.add(critere)
        db.session.commit()

        return critere