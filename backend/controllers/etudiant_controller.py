from flask import Blueprint, request, jsonify
from flasgger import swag_from

from services.etudiant_service import EtudiantService

etudiant_bp = Blueprint('etudiant_bp', __name__)


class EtudiantController:

    @staticmethod
    @etudiant_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Authentification'],
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