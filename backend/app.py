from flask import Flask
from flask_migrate import Migrate

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

app = Flask(__name__)

Swagger(app)
app.register_blueprint(etudiant_bp, url_prefix='/etudiant')
app.register_blueprint(comptable_bp, url_prefix='/comptable')

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