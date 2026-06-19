from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
import os
from config.database import db

from models.promotion import Promotion
from models.etudiant import Etudiant
from models.preuve_paiement import PreuvePaiement
from models.comptable import Comptable
from models.surveillant import Surveillant
from models.critere_paiement import CriterePaiement
from flasgger import Swagger

from controllers.etudiant_controller import EtudiantController, etudiant_bp
from controllers.comptable_controller import ComptableController, comptable_bp
from controllers.surveillant_controller import SurveillantController, surveillant_bp
from controllers.critere_controller import CritereController, critere_bp


app = Flask(__name__)
CORS(app)
Swagger(app)
app.register_blueprint(etudiant_bp, url_prefix='/etudiant')
app.register_blueprint(comptable_bp, url_prefix='/comptable')
app.register_blueprint(surveillant_bp, url_prefix='/surveillant')
app.register_blueprint(critere_bp, url_prefix='/critere')


# Configuration pour les fichiers téléchargés
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

# Configuration MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/droit_acces'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
# Initialisation
db.init_app(app)

# Migration
migrate = Migrate(app, db)

# Route test
@app.route("/")
def home():
    return "Application OK"


if __name__ == "__main__":
    print("Serveur Flask démarré...")
    app.run(debug=True)