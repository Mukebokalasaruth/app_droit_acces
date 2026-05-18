from flask import Blueprint, request, jsonify
from flasgger import swag_from

from services.comptable_service import ComptableService

comptable_bp = Blueprint('comptable_bp', __name__)


class ComptableController:

    @staticmethod
    @comptable_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Authentification'],
        'description': 'Connexion comptable',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'login': {
                            'type': 'string',
                            'example': 'comptable1'
                        },
                        'password': {
                            'type': 'string',
                            'example': '1234'
                        }
                    },
                    'required': ['login', 'password']
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
    def login_comptable():
        try:
            data = request.get_json()

            comptable = ComptableService.login_comptable(data)

            if comptable:

                return jsonify({
                    "success": True,
                    "message": "Connexion réussie",
                    "data": {
                        "id": comptable.id,
                        "login": comptable.login,
                        "nom": comptable.nom,
                        "prenom": comptable.prenom,
                    }
                }), 200

            return jsonify({
                "success": False,
                "message": "login ou mot de passe incorrect"
            }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "success": False,
                "message": "erreur serveur"
            }), 500