from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    economic_class: str = Field(default="middle")
    moral_class: str = Field(default="average")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    player: dict
