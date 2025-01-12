from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app import mongo
from app.models import RegistrationDto, ServiceResultDto, AuthenticationDto
from app.services import MembershipService

# Define Blueprints
register = Blueprint('register', __name__, url_prefix='/register')
authenticate = Blueprint('authenticate', __name__, url_prefix='/authenticate')
service_controller = Blueprint('service_controller', __name__, url_prefix='/service')

# ServiceController Class with static status variable
class ServiceController:
    status = "stopped"  # Default status is "stopped"

# User Registration - POST
@register.route('', methods=["POST"])
@swag_from({
    'tags': ['User Registration'],
    'description': 'Endpoint to register a new user.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'},
                    'mobile_number': {'type': 'string'},
                    'address': {
                        'type': 'object',
                        'properties': {
                            'street': {'type': 'string'},
                            'city': {'type': 'string'},
                            'state': {'type': 'string'},
                            'post_code': {'type': 'string'},
                            'country': {'type': 'string'}
                        }
                    },
                    'user_type': {'type': 'string', 'enum': ['JobSeeker', 'Recruiter', 'Employee']}
                },
                'required': ['email', 'password', 'first_name', 'last_name']
            }
        }
    ],
    'responses': {
        200: {'description': 'User registered successfully'},
        400: {'description': 'Validation error'},
        500: {'description': 'Server error'}
    }
})
def register_user():
    try:
        data = request.json
        registration_dto = RegistrationDto(**data)
        
        # Check if user already exists
        if mongo.db.users.find_one({"email": registration_dto.email}):
            return jsonify({"status_code": 400, "message": "Email already exists.", "data": False})
        
        # Hash password and store user data
        registration_dto.password = registration_dto.password
        user_data = registration_dto.dict()
        
        mongo.db.users.insert_one(user_data)
        return jsonify({"status_code": 200, "message": "User registered successfully.", "data": True})
    except Exception as e:
        return jsonify({"status_code": 500, "message": str(e), "data": False})


# Authentication Controller - POST
@authenticate.route('', methods=["POST"])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Authenticate a user.',
    'parameters': [
        {
            'name': 'email',
            'in': 'query',
            'required': True,
            'type': 'string',
            'description': 'The email of the user.'
        },
        {
            'name': 'password',
            'in': 'query',
            'required': True,
            'type': 'string',
            'description': 'The password of the user.'
        }
    ],
    'responses': {
        200: {'description': 'Authentication successful'},
        401: {'description': 'Unauthorized (wrong credentials)'},
        500: {'description': 'Server error'}
    }
})
def authenticate_user_post():
    try:
        email = request.args.get('email')
        password = request.args.get('password')

        if not email or not password:
            return jsonify({"status_code": 400, "message": "Email and password are required.", "data": False})

        user = mongo.db.users.find_one({"email": email})

        if user and user["password"] == password:
            return jsonify({
                "status_code": 200,
                "message": "Authentication successful!",
                "data": {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "mobile_number": user["mobile_number"],
                    "address": user["address"],
                    "user_type": user["user_type"]
                }
            })

        return jsonify({"status_code": 401, "message": "Invalid credentials.", "data": False})

    except Exception as e:
        return jsonify({"status_code": 500, "message": str(e), "data": False})


# Authentication Controller - GET (For Query Parameters)
@authenticate.route('/get', methods=["GET"])
@swag_from({
    'tags': ['Authentication'],
    'description': 'Authenticate a user using GET request with email and password as query parameters.',
    'parameters': [
        {
            'name': 'email',
            'in': 'query',
            'required': True,
            'type': 'string',
            'description': 'The email of the user.'
        },
        {
            'name': 'password',
            'in': 'query',
            'required': True,
            'type': 'string',
            'description': 'The password of the user.'
        }
    ],
    'responses': {
        200: {'description': 'Authentication successful'},
        401: {'description': 'Unauthorized (wrong credentials)'},
        500: {'description': 'Server error'}
    }
})
def authenticate_user_get():
    try:
        email = request.args.get('email')
        password = request.args.get('password')

        if not email or not password:
            return jsonify({"status_code": 400, "message": "Email and password are required.", "data": False})

        user = mongo.db.users.find_one({"email": email})

        if user and user["password"] == password:
            return jsonify({
                "status_code": 200,
                "message": "Authentication successful!",
                "data": {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "mobile_number": user["mobile_number"],
                    "address": user["address"],
                    "user_type": user["user_type"]
                }
            })

        return jsonify({"status_code": 401, "message": "Invalid credentials.", "data": False})

    except Exception as e:
        return jsonify({"status_code": 500, "message": str(e), "data": False})


# Service Controller - Start
@service_controller.route('/start', methods=["GET"])
@swag_from({
    'tags': ['Service'],
    'description': 'Start the service.',
    'responses': {
        200: {'description': 'Service started successfully.'},
        500: {'description': 'Server error'}
    }
})
def start_service():
    ServiceController.status = "started"  # Access the class variable
    return jsonify({"status_code": 200, "message": "Service started successfully.", "data": True})

# Service Controller - Stop
@service_controller.route('/stop', methods=["GET"])
@swag_from({
    'tags': ['Service'],
    'description': 'Stop the service.',
    'responses': {
        200: {'description': 'Service stopped successfully.'},
        500: {'description': 'Server error'}
    }
})
def stop_service():
    ServiceController.status = "stopped"  # Access the class variable
    return jsonify({"status_code": 200, "message": "Service stopped successfully.", "data": True})

# Service Controller - Status
@service_controller.route('/status', methods=["GET"])
@swag_from({
    'tags': ['Service'],
    'description': 'Check the service status.',
    'responses': {
        200: {'description': 'Service status checked successfully.'},
        500: {'description': 'Server error'}
    }
})
def check_service_status():
    return jsonify({"status_code": 200, "message": f"Service is {ServiceController.status}.", "data": True})
