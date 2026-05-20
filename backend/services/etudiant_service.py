import os
import uuid

from werkzeug.utils import secure_filename

from repositories.etudiant_repository import (EtudiantRepository)


from repositories.preuvePaiement_repository import (  PreuvePaiementRepository)

  


class EtudiantService:

    # AUTHENTIFICATION ETUDIANT
    @staticmethod
    def login_etudiant(data):
        matricule = data.get('matricule')
        password = data.get('password')

        # Vérifier les informations d'identification de l'étudiant
        if not matricule or not password:
            raise ValueError("Matricule ou mot de passe sont requis")

        etudiant = EtudiantRepository.get_etudiant_by_matricule_and_password(matricule, password)

        if etudiant:
            return etudiant
        return None
    

    UPLOAD_FOLDER = 'uploads'


    # VERIFIER FORMAT FICHIER
    
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   
    



    # UPLOAD PREUVE PAIEMENT

    @staticmethod
    def upload_preuve_paiement(
        file,
        id_etudiant
    ):

        # vérifier étudiant
        if not id_etudiant:
            raise ValueError(
                "L'id étudiant est requis"
            )

        # vérifier fichier
        if not file:
            raise ValueError(
                "Aucun fichier envoyé"
            )

        if file.filename == '':
            raise ValueError(
                "Fichier invalide"
            )

        # vérifier extension
        if not EtudiantService.allowed_file(
            file.filename
        ):
            raise ValueError(
                "Format invalide. Utilisez png, jpg, jpeg ou pdf"
            )

        # créer dossier uploads si ce n'est pas déjâ fait
        os.makedirs(
            EtudiantService.UPLOAD_FOLDER,
            exist_ok=True
        )

        # générer nom unique ou renommer le nom du fichier (venant de l'utilisateur)pour éviter des conflits
        extension = (
            file.filename
            .rsplit('.', 1)[1]
            .lower()
        )

        unique_filename = (
            f"{uuid.uuid4()}.{extension}"
        )

        filename = secure_filename(
            unique_filename
        )

        filepath = os.path.join(
            EtudiantService
            .UPLOAD_FOLDER,
            filename
        )

        # sauvegarder fichier
        file.save(filepath)


        preuve_saved = (PreuvePaiementRepository.create(id_etudiant=id_etudiant,
                chemin_capture=filepath))

            
        return {
            "id":
                preuve_saved.id,
            "idEtudiant":
                preuve_saved.idEtudiant,
            "cheminCapture":
                preuve_saved.cheminCapture
        }
