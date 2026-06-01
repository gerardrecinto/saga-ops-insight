from signal_harbor.ports.cache import Cache
from signal_harbor.ports.signal_writer import SignalWriter


class SignalIngestionService:
    # SRP: only writes signals and invalidates cache — never reads or scores
    # DIP: depends on Protocol abstractions (SignalWriter, Cache), not concrete adapters

    def __init__(self, writer: SignalWriter, cache: Cache) -> None:
        self._writer = writer
        self._cache = cache

    def ingest(self, signal: dict) -> dict:
        saved = self._writer.save(signal)

        # invalidate so the next risk-summary fetch reflects this new signal
        cache_key = f"risk:{signal['service_name'].lower()}"
        self._cache.delete(cache_key)

        return saved
