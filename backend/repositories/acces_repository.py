from config.database import db

from models.acces import Acces

class AccesRepository:

    # RECHERCHER ACCES PAR MATRICULE
    @staticmethod
    def get_acces_by_matricule(matricule):
        return Acces.query.filter_by(matriculeEtudiant=matricule).first()

    # AJOUTER UN MATRICULE
    @staticmethod
    def ajouter_matricule(matricule):

        existe = AccesRepository.get_acces_by_matricule(matricule)
        if existe:
            return None

        acces = Acces(matriculeEtudiant=matricule)
        db.session.add(acces)
        db.session.commit()
        return acces
    
    # SUPPRIMER TOUS LES MATRICULES
    @staticmethod
    def supprimer_tous_les_matricules():
        nombre = (Acces.query.delete())
        db.session.commit()
        return nombre