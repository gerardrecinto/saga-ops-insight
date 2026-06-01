from datetime import datetime
from typing import Protocol, runtime_checkable


@runtime_checkable
class SignalReader(Protocol):
    # ISP: read-only surface — callers that score risk never gain write access through this port
    def find_by_service_after(
        self, service_name: str, after: datetime
    ) -> list[dict]:
        """Return signals for *service_name* observed after *after*, as plain dicts."""
        ...
