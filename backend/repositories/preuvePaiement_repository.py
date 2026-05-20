from config.database import db
from models.preuve_paiement import PreuvePaiement
from models.etudiant import Etudiant


class PreuvePaiementRepository:

    # CREER PREUVE PAIEMENT
    @staticmethod
    def create(id_etudiant, chemin_capture):
        preuve_paiement = PreuvePaiement(
            idEtudiant=id_etudiant,
            cheminCapture=chemin_capture
        )
        db.session.add(preuve_paiement)
        db.session.commit()
        return preuve_paiement

    