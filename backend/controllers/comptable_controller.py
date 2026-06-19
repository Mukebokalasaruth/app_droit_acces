from flask import (
    Blueprint,
    request,
    jsonify
)

from flasgger import (
    swag_from
)

from services.comptable_service import (
    ComptableService
)


comptable_bp = Blueprint(
    'comptable_bp',
    __name__
)


class ComptableController:


    # ==========================
    # LOGIN COMPTABLE
    # ==========================
    @staticmethod
    @comptable_bp.route('/login', methods=['POST'])
    @swag_from({
        'tags': ['Comptable'],
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

                    'required': [
                        'login',
                        'password'
                    ]
                }
            }
        ],

        'responses': {

            200: {
                'description':
                    'Connexion réussie'
            },

            401: {
                'description':
                    'Erreur authentification'
            },

            500: {
                'description':
                    'Erreur serveur'
            }
        }
    })
    def login_comptable():

        try:

            data = (
                request.get_json()
            )

            comptable = (
                ComptableService
                .login_comptable(
                    data
                )
            )

            if comptable:

                return jsonify({

                    "success": True,

                    "message":
                        "Connexion réussie",

                    "data": {

                        "id":
                            comptable.id,

                        "login":
                            comptable.login,

                        "nom":
                            comptable.nom,

                        "prenom":
                            comptable.prenom
                    }

                }), 200

            return jsonify({

                "success": False,

                "message":
                    "Login ou mot de passe incorrect"

            }), 401

        except Exception as e:

            return jsonify({

                "success": False,

                "message":
                    str(e)

            }), 500


    # ==========================
    # LISTE PROMOTIONS
    # ==========================
    @staticmethod
    @comptable_bp.route('/promotions',methods=['GET'])
    @swag_from({
        'tags': ['Comptable'],
        'description':
            'Lister toutes les promotions',

        'responses': {

            200: {
                'description':
                    'Liste des promotions'
            },

            400: {
                'description':
                    'Erreur'
            }
        }
    })
    def get_promotions():

        try:

            result = (
                ComptableService
                .get_promotions()
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


    # ==========================
    # PREUVES PAR PROMOTION
    # ==========================
    @staticmethod
    @comptable_bp.route(
        '/preuves-promotion/<int:id_promotion>',
        methods=['GET']
    )
    @swag_from({
        'tags': ['Comptable'],
        'description':
            'Lister les preuves de paiement d’une promotion',

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
                    'Liste des preuves'
            },

            400: {
                'description':
                    'Erreur'
            }
        }
    })
    def get_preuves_by_promotion(
        id_promotion
    ):

        try:

            result = (
                ComptableService
                .get_preuves_by_promotion(
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


    # ==========================
    # APPROUVER PAIEMENT
    # ==========================
    @staticmethod
    @comptable_bp.route(
        '/approuver-paiement/<int:id_preuve>',
        methods=['PUT']
    )
    @swag_from({
        'tags': ['Comptable'],
        'description':
            'Approuver une preuve de paiement',

        'parameters': [
            {
                'name':
                    'id_preuve',

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
                    'Paiement approuvé'
            },

            400: {
                'description':
                    'Erreur'
            }
        }
    })
    def approuver_paiement(
        id_preuve
    ):

        try:

            result = (
                ComptableService
                .approuver_paiement(
                    id_preuve
                )
            )

            return jsonify({

                "success": True,

                "message":
                    "Paiement approuvé",

                "data":
                    result

            }), 200

        except Exception as e:

            return jsonify({

                "success": False,

                "message":
                    str(e)

            }), 400


    # ==========================
    # REJETER PAIEMENT
    # ==========================
    @staticmethod
    @comptable_bp.route(
        '/rejeter-paiement/<int:id_preuve>',
        methods=['PUT']
    )
    @swag_from({
        'tags': ['Comptable'],
        'description':
            'Rejeter une preuve de paiement',

        'parameters': [
            {
                'name':
                    'id_preuve',

                'in':
                    'path',

                'required':
                    True,

                'type':
                    'integer',

                'example':
                    1
            },
            {
                'name':
                    'body',

                'in':
                    'body',

                'required':
                    True,

                'schema': {

                    'type':
                        'object',

                    'properties': {

                        'motifRejet': {

                            'type':
                                'string',

                            'example':
                                'Capture illisible'
                        }
                    },

                    'required': [
                        'motifRejet'
                    ]
                }
            }
        ],

        'responses': {

            200: {
                'description':
                    'Paiement rejeté'
            },

            400: {
                'description':
                    'Erreur'
            }
        }
    })
    def rejeter_paiement(
        id_preuve
    ):

        try:

            data = (
                request.get_json(
                    silent=True
                )
            )

            if not data:

                return jsonify({

                    "success": False,

                    "message":
                        "Aucune donnée JSON envoyée"

                }), 400


            motif_rejet = (
                data.get(
                    'motifRejet'
                )
            )

            result = (
                ComptableService
                .rejeter_paiement(
                    id_preuve,
                    motif_rejet
                )
            )

            return jsonify({

                "success": True,

                "message":
                    "Paiement rejeté",

                "data":
                    result

            }), 200

        except Exception as e:

            return jsonify({

                "success": False,

                "message":
                    str(e)

            }), 400