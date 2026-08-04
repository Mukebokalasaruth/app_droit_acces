from flask import Blueprint, request, jsonify
from flasgger import swag_from

from services.etudiant_service import EtudiantService

etudiant_bp = Blueprint('etudiant_bp', __name__)


class EtudiantController:

    @staticmethod
    @etudiant_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Etudiant'],
        'description': 'Connexion étudiant',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'matricule': {
                            'type': 'string',
                            'example': '22MK289'
                        },
                        'password': {
                            'type': 'string',
                            'example': '1234'
                        }
                    },
                    'required': ['matricule', 'password']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Connexion réussie'
            },
            401: {
                'description': 'Erreur de validation'
            },
            500: {
                'description': 'Erreur serveur'
            }
        }
    })
    def login_etudiant():
        try:
            data = request.get_json()

            etudiant = EtudiantService.login_etudiant(data)

            if etudiant:

                return jsonify({
                    "success": True,
                    "message": "Connexion réussie",
                    "data": {
                        "id": etudiant.id,
                        "nom": etudiant.nom,
                        "postnom": etudiant.postnom,
                        "prenom": etudiant.prenom,
                        "matricule": etudiant.matricule
                    }
                }), 200

            return jsonify({
                "success": False,
                "message": "Matricule ou mot de passe incorrect"
            }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "success": False,
                "message": "erreur serveur"
            }), 500
        
    # UPLOAD PREUVE PAIEMENT
    # ==========================
    @staticmethod
    @etudiant_bp.route('/upload-preuve', methods=['POST'])
    @swag_from({
        'tags': ['Etudiant'],
        'consumes': ['multipart/form-data'],
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description':
                    'Capture preuve paiement'
            },
            {
                'name': 'idEtudiant',
                'in': 'formData',
                'type': 'integer',
                'required': True,
                'description':
                    'ID étudiant'
            }
        ],
        'responses': {
            201: {
                'description':
                    'Preuve envoyée avec succès'
            },
            400: {
                'description':
                    'Erreur validation'
            },
            500: {
                'description':
                    'Erreur serveur'
            }
        }
    })
    def upload_preuve():

        try:

            # récupérer fichier
            file = request.files.get(
                'file'
            )

            # récupérer id étudiant
            id_etudiant = request.form.get(
                'idEtudiant'
            )

            # appel service
            result = (
                EtudiantService
                .upload_preuve_paiement(
                    file,
                    id_etudiant
                )
            )

            return jsonify({
                "success": True,
                "message":
                    "Preuve de paiement envoyée avec succès",
                "data":
                    result
            }), 201

        except ValueError as e:

            return jsonify({
                "success": False,
                "message":
                    str(e)
            }), 400

        except Exception as e:

            return jsonify({
                "success": False,
                "message":
                    str(e)
            }), 500
        
        # ==========================
    # CONSULTER ETAT VALIDATION
    # ==========================
    @staticmethod
    @etudiant_bp.route(
        '/etat-validation/<int:id_etudiant>',
        methods=['GET']
    )
    def consulter_etat_validation(
        id_etudiant
    ):

        try:

            result = (
                EtudiantService
                .consulter_etat_validation(
                    id_etudiant
                )
            )

            return jsonify({

                "success": True,

                "data":
                    result

            }), 200

        except Exception as e:

            return jsonify({

                "success": False,

                "message":
                    str(e)

            }), 400

    @staticmethod
    @etudiant_bp.route(
        '/preuves-rejetees/<int:id_etudiant>',
        methods=['GET']
    )
    def get_preuves_rejetees(
        id_etudiant
    ):

        try:

            result = (
                EtudiantService
                .get_preuves_rejetees(
                    id_etudiant
                )
            )

            return jsonify({

                "success": True,

                "data":
                    result

            }), 200

        except Exception as e:

            return jsonify({

                "success": False,

                "message":
                    str(e)

            }), 400
