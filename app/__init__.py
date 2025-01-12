#__init__.py

from flask import Flask
from flask_pymongo import PyMongo
from config import Config

# Create PyMongo instance
mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize MongoDB
    mongo.init_app(app)
    
    # Import routes and register Blueprints after initializing Flask app
    from app.controllers import register, authenticate, service_controller
    app.register_blueprint(register)
    app.register_blueprint(authenticate)
    app.register_blueprint(service_controller)
    
    return app