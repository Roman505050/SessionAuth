from enum import StrEnum

from application.code.utils.key_formater import KeyFormater


class EmailCodeType(StrEnum):
    VERIFICATION = "verification"
    EMAIL_CHANGE = "email_change"


EMAIL_CODE_FORMATS = {
    EmailCodeType.VERIFICATION: KeyFormater(
        "email_code:verification:{user_uuid}"
    ),
    EmailCodeType.EMAIL_CHANGE: KeyFormater(
        "email_code:email_change:{email_type}:{request_uuid}"
    ),  # email_type: old or new
}

EMAIL_CODE_REQUIRED_FIELDS = {
    EmailCodeType.VERIFICATION: ["user_uuid"],
    EmailCodeType.EMAIL_CHANGE: ["email_type", "request_uuid"],
}
