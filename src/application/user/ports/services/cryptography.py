from abc import ABC, abstractmethod


class ICryptographyService(ABC):
    @abstractmethod
    def generate_salt(self) -> str:
        pass

    @abstractmethod
    def hash_password(self, password: str, salt: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        pass
