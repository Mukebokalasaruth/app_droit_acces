from repositories.comptable_repository import ComptableRepository

class ComptableService:

    # AUTHENTIFICATION COMPTABLE
    @staticmethod
    def login_comptable(data):
        login = data.get('login')
        password = data.get('password')

        # Vérifier les informations d'identification du comptable
        if not login or not password:
            raise ValueError("Login et mot de passe sont requis")

        comptable = ComptableRepository.get_comptable_by_login_and_password(login, password)

        if comptable:
            return comptable
        return None