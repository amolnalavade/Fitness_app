from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)

from routes import auth, admin, trainer, client, membership

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(trainer.bp)
app.register_blueprint(client.bp)
app.register_blueprint(membership.bp)

if __name__ == '__main__':
    app.run(debug=True)