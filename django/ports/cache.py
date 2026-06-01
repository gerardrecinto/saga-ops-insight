from typing import Optional, Protocol, runtime_checkable


@runtime_checkable
class Cache(Protocol):
    # ISP: minimal surface — services only need get/set/delete, not the full Redis command set
    def get(self, key: str) -> Optional[str]:
        ...

    def set(self, key: str, value: str, ttl_seconds: int) -> None:
        ...

    def delete(self, key: str) -> None:
        ...
