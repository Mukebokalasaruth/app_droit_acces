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
        
        

    