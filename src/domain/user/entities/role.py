from dataclasses import dataclass, field

from shared.domain.entity import Entity


@dataclass
class RoleEntity(Entity):
    name: str

    def __post_init__(self):
        self._validate_name()

    def _validate_name(self):
        if not 3 <= len(self.name) <= 64:
            raise ValueError("Name must be between 3 and 64 characters")

    def __repr__(self):
        return f"<Role uuid={self.uuid} name={self.name}>"
