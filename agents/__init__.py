# Response structure and shared constants

from dataclasses import dataclass, asdict
from typing import Any, Optional

@dataclass
class Response:
    success: bool
    message: str
    data: Optional[Any] = None

    def to_dict(self):
        return asdict(self)

# Shared Constraints
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000
