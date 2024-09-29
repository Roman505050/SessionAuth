from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UserAgent:
    browser: Optional[str]
    browser_version: Optional[str]
    os: Optional[str]
    device: Optional[str]
