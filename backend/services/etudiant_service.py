from repositories.etudiant_repository import EtudiantRepository


class EtudiantService:

    # AUTHENTIFICATION ETUDIANT
    @staticmethod
    def login_etudiant(data):
        matricule = data.get('matricule')
        password = data.get('password')

        # Vérifier les informations d'identification de l'étudiant
        if not matricule or not password:
            raise ValueError("Matricule et mot de passe sont requis")

        etudiant = EtudiantRepository.get_etudiant_by_matricule_and_password(matricule, password)

        if etudiant:
            return etudiant
        return None
        
        

        