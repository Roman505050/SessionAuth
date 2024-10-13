from abc import ABC, abstractmethod

from application.session.ports.repositories.session import ISessionRepository
from application.user.ports.repositories.user import IUserRepository


class IUnitOfWork(ABC):
    user_repo: IUserRepository
    session_repo: ISessionRepository

    @abstractmethod
    def __init__(self): ...

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...

    @abstractmethod
    async def close(self): ...
