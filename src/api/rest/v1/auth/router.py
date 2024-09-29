from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from loguru import logger

from api.rest.v1.auth.dependencies import (
    get_user_service,
    get_session_service,
    get_user_agent,
    get_ip_remote,
)
from api.rest.v1.auth.schemas import RegisterResponse
from application.session.dto.session import SessionDTO
from application.session.services.session_service import SessionService
from application.user.dto.register_user import RegisterUser
from application.user.services.user_service import UserService
from domain.session.value_objects.user_agent import UserAgent
from shared.exceptions.already_exist import AlreadyExistException
from shared.validators.email import EmailNotValidError

from config import session_settings

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=RegisterResponse,
)
async def register(
    response: Response,
    body: RegisterUser,
    user_agent: UserAgent = Depends(get_user_agent),
    ip_address: str = Depends(get_ip_remote),
    user_service: UserService = Depends(get_user_service),
    session_service: SessionService = Depends(get_session_service),
):
    try:
        user = await user_service.register(body)

        sessions, current_session = await session_service.create(
            user=user, user_agent=user_agent, ip_address=ip_address
        )

        response.set_cookie(
            key="session_id",
            value=current_session.session_id,
            httponly=True,
            secure=True,
            samesite="strict",
            path="/",
            max_age=session_settings.expire_seconds,
        )

        return RegisterResponse(
            message="Check your email box to verify your email.",
            user=user,
            sessions=sessions
            + [SessionDTO.from_entity(current_session, is_current=True)],
        )
    except AlreadyExistException as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
            },
        )
    except EmailNotValidError:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Email is not valid.",
            },
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
            },
        )
    except Exception as e:
        logger.error(f"Register user error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Something went wrong.",
            },
        )
