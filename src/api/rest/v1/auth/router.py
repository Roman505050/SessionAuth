from fastapi import APIRouter, Depends, status, Response, Body, Request
from fastapi.responses import JSONResponse
from email_validator import EmailNotValidError
from loguru import logger

from api.rest.v1.auth.dependencies import (
    get_user_service,
    get_user_agent,
    get_ip_remote,
)
from api.rest.v1.auth.schemas import (
    RegisterResponse,
    ConfirmEmailResponse,
    CodeRequest,
)
from application.code.exceptions.code_expired import EmailCodeExpiredException
from application.code.exceptions.code_invalid import EmailCodeInvalidException
from application.user.dto.register_user import RegisterUser
from application.user.services.user_service import UserService
from domain.session.value_objects.user_agent import UserAgent
from shared.exceptions.already_exist import AlreadyExistException
from shared.validators.email import EmailLengthNotValidError

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
):
    try:
        user, sessions, session_id = await user_service.register(
            body, user_agent, ip_address
        )

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=session_settings.SECURE,
            samesite="strict",
            path="/",
            max_age=session_settings.EXPIRE_SECONDS,
        )

        return RegisterResponse(
            message="Check your email box to verify your email.",
            user=user,
            sessions=sessions,
        )
    except AlreadyExistException as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
            },
        )
    except EmailLengthNotValidError as e:
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


@router.post(
    "/confirm-email",
    status_code=status.HTTP_200_OK,
    response_model=ConfirmEmailResponse,
)
async def confirm_email(
    request: Request,
    data: CodeRequest,
    user_service: UserService = Depends(get_user_service),
):
    session_id = request.cookies.get("session_id", None)
    if not session_id:
        # 401 Unauthorized
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "message": "Unauthorized",
            },
        )

    try:
        user = await user_service.verify_email(session_id, data.code)

        return ConfirmEmailResponse(
            message="Email confirmed successfully.",
            user=user,
        )
    except EmailCodeExpiredException as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
            },
        )
    except EmailCodeInvalidException as e:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": str(e),
            },
        )
    except Exception as e:
        logger.error(f"Confirm email error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Something went wrong.",
            },
        )
