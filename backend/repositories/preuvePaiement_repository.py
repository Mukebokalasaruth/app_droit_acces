from config.database import db

from models.preuve_paiement import (
    PreuvePaiement
)

from models.etudiant import (
    Etudiant
)


class PreuvePaiementRepository:


    # ==========================
    # CREER PREUVE PAIEMENT
    # ==========================
    @staticmethod
    def create(
        id_etudiant,
        chemin_capture
    ):

        preuve_paiement = (
            PreuvePaiement(
                idEtudiant=id_etudiant,
                cheminCapture=chemin_capture,
                statutValidation=None,
                motifRejet=None
            )
        )

        db.session.add(
            preuve_paiement
        )

        db.session.commit()

        return preuve_paiement


    # ==========================
    # PREUVES PAR PROMOTION
    # ==========================
    @staticmethod
    def get_preuves_by_promotion(
        id_promotion
    ):

        preuves = (

            db.session.query(

                PreuvePaiement,

                Etudiant.nom,
                Etudiant.postnom,
                Etudiant.prenom,
                Etudiant.matricule

            )

            .join(
                Etudiant,
                PreuvePaiement.idEtudiant
                == Etudiant.id
            )

            .filter(
                Etudiant.idPromotion
                == id_promotion
            )

            .order_by(
                PreuvePaiement
                .dateSoumission
                .asc()
            )

            .all()
        )

        return preuves


    # ==========================
    # APPROUVER PAIEMENT
    # ==========================
    @staticmethod
    def approuver_paiement(
        id_preuve
    ):

        preuve = (
            PreuvePaiement
            .query
            .get(id_preuve)
        )

        if not preuve:
            return None

        preuve.statutValidation = True

        preuve.motifRejet = None

        db.session.commit()

        return preuve


    # ==========================
    # REJETER PAIEMENT
    # ==========================
    @staticmethod
    def rejeter_paiement(
        id_preuve,
        motif_rejet
    ):

        preuve = (
            PreuvePaiement
            .query
            .get(id_preuve)
        )

        if not preuve:
            return None

        preuve.statutValidation = False

        preuve.motifRejet = (
            motif_rejet
        )

        db.session.commit()

        return preuve
