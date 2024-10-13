from pydantic import BaseModel, Field

from application.session.dto.session import SessionDTO
from application.user.dto.user import UserDTO


class CodeRequest(BaseModel):
    code: str = Field(
        ...,
        json_schema_extra={
            "example": {
                "code": "123456",
            }
        },
        description="Code from email",
        min_length=6,
        max_length=6,
    )


class RegisterResponse(BaseModel):
    success: bool = True
    message: str = "User registered successfully."
    user: UserDTO
    sessions: list[SessionDTO]


class ConfirmEmailResponse(BaseModel):
    success: bool = True
    message: str = "Email confirmed successfully."
    user: UserDTO
