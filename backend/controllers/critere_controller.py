from flask import Blueprint, request, jsonify
from flasgger import swag_from
from services.critere_service import CriterePaiementService

critere_bp = Blueprint("critere_bp", __name__)


class CritereController:

    # FIXER CRITERE PAIEMENT
    @staticmethod
    @critere_bp.route("/critere-paiement", methods=["POST"])
    @swag_from({
        "tags": ["Comptable"],
        "description": "Fixer le critère de paiement",

        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "montant": {
                            "type": "integer",
                            "example": 50000
                        },
                        "session": {
                            "type": "string",
                            "example": "premiere session"
                        },
                        "idPromotion": {
                            "type": "integer",
                            "example": 1
                        }
                    },
                    "required": ["montant", "session", "idPromotion"]
                }
            }
        ],

        "responses": {
            201: {"description": "Critère créé"},
            400: {"description": "Erreur"}
        }
    })
    def fixer_critere():

        try:
            data = request.get_json()

            critere = CriterePaiementService.fixer_critere(data)

            return jsonify({
                "success": True,
                "message": "Critère de paiement fixé avec succès",
                "data": {
                    "id": critere.id,
                    "montant": critere.montant,
                    "session": critere.session,
                    "idPromotion": critere.idPromotion
                }
            }), 201

        except Exception as e:
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400