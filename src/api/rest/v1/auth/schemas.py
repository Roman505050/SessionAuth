from pydantic import BaseModel

from application.session.dto.session import SessionDTO
from application.user.dto.user import UserDTO


class RegisterResponse(BaseModel):
    success: bool = True
    message: str = "User registered successfully."
    user: UserDTO
    sessions: list[SessionDTO]
