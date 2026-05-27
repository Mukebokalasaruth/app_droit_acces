from repositories.comptable_repository import (
    ComptableRepository
)

from repositories.promotion_repository import (
    PromotionRepository
)

from repositories.preuvePaiement_repository import (
    PreuvePaiementRepository
)


class ComptableService:


    # ==========================
    # AUTHENTIFICATION COMPTABLE
    # ==========================
    @staticmethod
    def login_comptable(
        data
    ):

        login = data.get(
            'login'
        )

        password = data.get(
            'password'
        )

        # vérifier données
        if not login or not password:

            raise ValueError(
                "Login et mot de passe sont requis"
            )

        comptable = (

            ComptableRepository
            .get_comptable_by_login_and_password(
                login,
                password
            )
        )

        if comptable:
            return comptable

        return None


    # ==========================
    # LISTE PROMOTIONS
    # ==========================
    @staticmethod
    def get_promotions():

        promotions = (

            PromotionRepository
            .get_all()
        )

        result = []

        for promotion in promotions:

            result.append({

                "id":
                    promotion.id,

                "nom":
                    promotion.nom
            })

        return result


    # ==========================
    # PREUVES D'UNE PROMOTION
    # ==========================
    @staticmethod
    def get_preuves_by_promotion(
        id_promotion
    ):

        preuves = (

            PreuvePaiementRepository
            .get_preuves_by_promotion(
                id_promotion
            )
        )

        result = []

        for (
            preuve,
            nom,
            postnom,
            prenom,
            matricule
        ) in preuves:

            result.append({

                "idPreuve":
                    preuve.id,

                "nom":
                    nom,

                "postnom":
                    postnom,

                "prenom":
                    prenom,

                "matricule":
                    matricule,

                "cheminCapture":
                    preuve.cheminCapture,

                "dateSoumission":
                    preuve.dateSoumission.strftime(
                        "%d/%m/%Y à %H:%M:%S"
                    ),

                "statutValidation":
                    preuve.statutValidation
            })

        return result


    # ==========================
    # APPROUVER PAIEMENT
    # ==========================
    @staticmethod
    def approuver_paiement(
        id_preuve
    ):

        preuve = (
            PreuvePaiementRepository
            .approuver_paiement(
                id_preuve
            )
        )

        if not preuve:

            raise ValueError(
                "Preuve introuvable"
            )

        return {

            "idPreuve":
                preuve.id,

            "statutValidation":
                preuve.statutValidation,

            "message":
                "Paiement approuvé"
        }


    # ==========================
    # REJETER PAIEMENT
    # ==========================
    @staticmethod
    def rejeter_paiement(
        id_preuve,
        motif_rejet
    ):

        if not motif_rejet:

            raise ValueError(
                "Motif rejet requis"
            )

        preuve = (
            PreuvePaiementRepository
            .rejeter_paiement(
                id_preuve,
                motif_rejet
            )
        )

        if not preuve:

            raise ValueError(
                "Preuve introuvable"
            )

        return {

            "idPreuve":
                preuve.id,

            "statutValidation":
                preuve.statutValidation,

            "motifRejet":
                preuve.motifRejet,

            "message":
                "Paiement rejeté"
        }