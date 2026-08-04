from flask import Blueprint, request, jsonify
from flasgger import swag_from


from services.surveillant_service import SurveillantService

surveillant_bp = Blueprint('surveillant_bp', __name__)


class SurveillantController:

    @staticmethod
    @surveillant_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Surveillant'],
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
    @staticmethod
    @surveillant_bp.route("/verifier-droit-acces/<string:matricule>",  methods=["GET"]) 
    @swag_from({
        'tags': ['Surveillant'],
        'description': 'Vérifier droit d\'accès étudiant',
        'parameters': [
            {
                'name': 'matricule',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Matricule de l\'étudiant',
                'example': '2023-12345'
            }
        ],
        'responses': {
            200: {
                'description': 'Vérification réussie'
            },
            400: {
                'description': 'Erreur de validation'
            },
            500: {
                'description': 'Erreur serveur'
            }
        }
    })  
    def verifier_droit_acces(matricule):
        try:

            result = (
                SurveillantService
                .verifier_droit_acces(
                    matricule
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
    @surveillant_bp.route('/vider-acces', methods=['POST'])
    @swag_from({
        'tags': ['Surveillant'],
        'description': 'Vider le registre des matricules entrés aujourd’hui',
        'responses': {
            200: {
                'description': 'Registre vidé avec succès'
            },
            500: {
                'description': 'Erreur serveur'
            }
        }
    })
    def vider_acces():
        try:
            nombre = SurveillantService.vider_acces()
            return jsonify({
                "success": True,
                "message": f"{nombre} accès(s) supprimé(s) avec succès"
            }), 200
        except Exception as e:
            return jsonify({
                "success": False,
                "message": str(e)
            }), 500
        

    # VERIFIER PAR PROMOTION

    @staticmethod
    @surveillant_bp.route('/verifier-par-promotion/<int:id_promotion>', methods=['GET'])    
    @swag_from({
        'tags': ['Surveillant'],
        'description':
            "Lister les étudiants validés d'une promotion",

        'parameters': [
            {
                'name':
                    'id_promotion',

                'in':
                    'path',

                'required':
                    True,

                'type':
                    'integer',

                'example':
                    1
            }
        ],

        'responses': {

            200: {
                'description':
                    'Liste des étudiants validés'
            }
        }
    })
    def verifier_par_promotion(id_promotion):
        try:

            result = (
                SurveillantService
                .verifier_par_promotion(
                    id_promotion
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