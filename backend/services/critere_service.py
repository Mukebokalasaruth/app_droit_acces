from repositories.criterePaiement_repository import CriterePaiementRepository


class CriterePaiementService:

    @staticmethod
    def fixer_critere(data):

        montant = data.get("montant")
        session = "Premiere session"
        id_promotion = data.get("idPromotion")

        return CriterePaiementRepository.create(
            montant,
            session,
            id_promotion
        )