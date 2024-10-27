from email_validator import (
    validate_email as vld_email,
)

from shared.validators.email.exeptions import (
    EmailLengthNotValidError,
)


def validate_email(email: str) -> str:
    if not 5 <= len(email) <= 320:
        raise EmailLengthNotValidError(
            "Email length must be between 5 and 320 characters."
        )
    valid = vld_email(email)
    return valid.normalized
