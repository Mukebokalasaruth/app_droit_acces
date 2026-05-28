from repositories.surveillant_repository import SurveillantRepository

class SurveillantService:

    # AUTHENTIFICATION SURVEILLANT
    @staticmethod
    def login_surveillant(data):
        login = data.get('login')
        password = data.get('password')

        # Vérifier les informations d'identification du surveillant
        if not login or not password:
            raise ValueError("Login et mot de passe sont requis")

        surveillant = SurveillantRepository.get_surveillant_by_login_and_password(login, password)

        if surveillant:
            return surveillant
        return None
    
    # VERIFIER DROIT ACCES
    @staticmethod
    def verifier_droit_acces(
        matricule
    ):

        # chercher étudiant
        etudiant = (
            SurveillantRepository
            .get_etudiant_by_matricule(
                matricule
            )
        )

        if not etudiant:

            raise Exception(
                "Étudiant introuvable"
            )


        # récupérer dernière preuve
        preuve = (
            SurveillantRepository
            .get_last_preuve(
                etudiant.id
            )
        )


        # aucune preuve
        if not preuve:

            etat = "Aucun paiement"
            autorisation = False


        elif preuve.statutValidation is True:

            etat = "Validé"
            autorisation = True


        elif preuve.statutValidation is False:

            etat = "Rejeté"
            autorisation = False


        else:

            etat = "En attente"
            autorisation = False


        return {

            "nom":
                etudiant.nom,

            "postnom":
                etudiant.postnom,

            "prenom":
                etudiant.prenom,

            "matricule":
                etudiant.matricule,

            "validite":
                etat,

            "autorisation":
                autorisation,

            "motifRejet":
                preuve.motifRejet
                if preuve else None
        }
        
        
    # LISTE VALIDES PAR PROMOTION
    @staticmethod
    def verifier_par_promotion(
        id_promotion
    ):

        etudiants = (
            SurveillantRepository
            .get_etudiants_valides_by_promotion(
                id_promotion
            )
        )

        if not etudiants:

            return []

        result = []

        for etudiant in etudiants:

            result.append({

                "id":
                    etudiant.id,

                "nom":
                    etudiant.nom,

                "postnom":
                    etudiant.postnom,

                "prenom":
                    etudiant.prenom,

                "matricule":
                    etudiant.matricule,

                "autorisation":
                    True
            })

        return result
        
        

    