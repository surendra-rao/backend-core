# backend/app/schemas.py
from pydantic import BaseModel, EmailStr

# Base schema (common attributes)
class UserBase(BaseModel):
    username: str
    email: EmailStr 

# Schema for creating a user (includes password)
class UserCreate(UserBase):
    password: str

# Schema for reading a user (hides password)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True # updated for Pydantic v2 (was orm_mode = True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str