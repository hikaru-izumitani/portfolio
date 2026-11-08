from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional

from rest_api.services.database.user_sql import UserSQL


@dataclass
class User:
    id: str
    name: str
    email: str
    updated: Optional[datetime] = field(default_factory=datetime.now)
    created: Optional[datetime] = field(default_factory=datetime.now)

    def to_user_sql(self) -> UserSQL:
        return UserSQL(
            id=self.id,
            name=self.name,
            email=self.email,
            created=self.created,
            updated=self.updated,
        )

    def to_dict(self) -> dict:
        data = asdict(self)
        for key in ("created", "updated"):
            value = data.get(key)
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data

    @classmethod
    def from_user_sql(cls, user_sql: UserSQL) -> "User":
        if not user_sql:
            return None
        return cls(
            id=user_sql.id,
            name=user_sql.name,
            email=user_sql.email,
            created=user_sql.created,
            updated=user_sql.updated,
        )
