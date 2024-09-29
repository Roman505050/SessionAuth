from enum import StrEnum


class Status(StrEnum):
    """
    Enum for the status of the verification code.
    """

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    EXPIRED = "expired"
