from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4
import datetime


@dataclass
class Entity(ABC):
    uuid: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime

    def __eq__(self, other):
        return isinstance(other, Entity) and self.uuid == other.uuid

    def __hash__(self):
        return hash(self.uuid)

    def __repr__(self):
        return f"{self.__class__.__name__}(uuid={self.uuid})"
