from pydantic import BaseModel, EmailStr, field_validator, ValidationError
from typing import Optional
import django.contrib.auth.password_validation as validators


class UserSignupSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    user_type: Optional[str] = 'user'

    @field_validator('password', mode='before')
    def validate_password(cls, value):
        try:
            validators.validate_password(value)
        except validators.ValidationError as e:
            raise ValueError(str(e))
        return value


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserUpdateSchema(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: Optional[str] = None
    password: Optional[str] = None


class UserResponseSchema(BaseModel):
    id : int
    email: EmailStr
    first_name: str
    last_name: str
    user_type: Optional[str]


class TokenResponseSchema(BaseModel):
    refresh: str
    access: str
    user_info: UserResponseSchema


class TokenRefreshSchema(BaseModel):
    refresh_token: str

