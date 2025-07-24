from dataclasses import dataclass, field
from datetime import datetime, date


@dataclass
class Validity:
    expire_in: date
    created_in: datetime = field(default_factory=datetime.now)

    def is_expired(self, now: date) -> bool:
        return now > self.expire_in