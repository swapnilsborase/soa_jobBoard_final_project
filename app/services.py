#services.py

from app.models import RegistrationDto, AuthenticationDto, ServiceResultDto
from app.utils import hash_password
from app import mongo
import uuid
from pymongo.errors import DuplicateKeyError

class MembershipService:

    @staticmethod
    def register(input_parameters: RegistrationDto) -> ServiceResultDto:
        # Check if email already exists
        if mongo.db.users.find_one({"email": input_parameters.email}):
            return ServiceResultDto(status_code=400, message="User's Email already exists!")

        # Hash password before saving
        input_parameters.password = hash_password(input_parameters.password)
        
        user_data = input_parameters.dict()
        user_data["id"] = str(uuid.uuid4())
        user_data["address"] = input_parameters.address.dict()

        try:
            mongo.db.users.insert_one(user_data)
            return ServiceResultDto(status_code=200, message="User's Registration successful", data=True)
        except DuplicateKeyError:
            return ServiceResultDto(status_code=500, message="An error occurred, try again!", data=False)

    @staticmethod
    def authenticate_user(input_parameters: AuthenticationDto) -> ServiceResultDto:
        user = mongo.db.users.find_one({"email": input_parameters.email, "password": input_parameters.password})
        
        if user:
            return ServiceResultDto(status_code=200, message="Authentication successful", data=True)
        else:
            return ServiceResultDto(status_code=401, message="Invalid credentials", data=False)