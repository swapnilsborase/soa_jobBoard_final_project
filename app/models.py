from pydantic import BaseModel, EmailStr, constr, root_validator
from enum import Enum
from typing import Optional
import uuid

class UserTypeEnum(str, Enum):
    JobSeeker = "JobSeeker"
    Recruiter = "Recruiter"
    Employee = "Employee"

class AddressDto(BaseModel):
    street: str
    city: str
    state: str
    post_code: str
    country: str

class UserBaseDto(BaseModel):
    id: Optional[str]  # Change this to a string
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: str
    address: AddressDto
    user_type: UserTypeEnum = UserTypeEnum.JobSeeker

    @root_validator(pre=True)
    def generate_id_if_missing(cls, values):
        if 'id' not in values:
            # Convert UUID to string
            values['id'] = str(uuid.uuid4())
        return values

class RegistrationDto(UserBaseDto):
    password: constr(min_length=8, max_length=20)

class AuthenticationDto(BaseModel):
    email: EmailStr
    password: str

class ServiceResultDto(BaseModel):
    status_code: int
    message: str
    data: Optional[bool] = None
