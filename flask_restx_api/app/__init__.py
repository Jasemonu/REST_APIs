from flask import Flask
from app.extensions import api, db
from app.resource import ns

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # Initialize the extensions
    api.init_app(app)
    db.init_app(app)

    # Add the namespace to the API
    api.add_namespace(ns)
    
    return app
