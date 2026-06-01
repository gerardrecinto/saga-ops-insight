from datetime import datetime

from signals.models import Signal


class DjangoSignalRepository:
    # SRP: only translates between domain dicts and Django ORM — no business logic
    # LSP: satisfies both SignalReader and SignalWriter Protocols
    # DIP: views and services depend on Protocol abstractions, not this concrete class

    def save(self, signal: dict) -> dict:
        obj = Signal.objects.create(
            service_name=signal["service_name"],
            environment=signal["environment"],
            signal_type=signal["signal_type"],
            severity=signal["severity"],
            observed_at=signal["observed_at"],
            summary=signal["summary"],
        )
        return obj.to_dict()

    def find_by_service_after(self, service_name: str, after: datetime) -> list[dict]:
        qs = Signal.objects.filter(
            service_name=service_name,
            observed_at__gte=after,
        )
        return [obj.to_dict() for obj in qs]
