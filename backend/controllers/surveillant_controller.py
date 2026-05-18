from flask import Blueprint, request, jsonify
from flasgger import swag_from


from services.surveillant_service import SurveillantService

surveillant_bp = Blueprint('surveillant_bp', __name__)


class SurveillantController:

    @staticmethod
    @surveillant_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Authentification'],
        'description': 'Connexion surveillant',
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
                            'example': 'surveillant1'
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
    def login_surveillant():
        try:
            data = request.get_json()

            surveillant = SurveillantService.login_surveillant(data)

            if surveillant:

                return jsonify({
                    "success": True,
                    "message": "Connexion réussie",
                    "data": {
                        "id": surveillant.id,
                        "prenom": surveillant.prenom,
                        "login": surveillant.login
                    }
                }), 200

            return jsonify({
                "success": False,
                "message": "Login ou mot de passe incorrect"
            }), 401

        except Exception as e:
            print(e)
            return jsonify({
                "success": False,
                "message": "erreur serveur"
            }), 500