from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    tl = "tl"

# What the frontend SENDS to login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# What the API RETURNS after login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str
    user_id: int

# What we return for a user profile
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True  # Lets Pydantic read SQLAlchemy objects