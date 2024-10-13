from pydantic import BaseModel, Field, EmailStr


class RegisterUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr = Field(..., min_length=5, max_length=320)
    password: str = Field(..., min_length=8, max_length=64)
