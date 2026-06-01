from typing import Protocol, runtime_checkable


@runtime_checkable
class SignalWriter(Protocol):
    # ISP: write-only surface — ingestion never needs query capability through this port
    def save(self, signal: dict) -> dict:
        """Persist *signal* and return the saved record (with generated id, etc.)."""
        ...
