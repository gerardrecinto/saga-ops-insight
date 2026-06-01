"""
PATTERN: Observer (Python implementation)

SignalEventBus is the Subject. Observers register a callable and are notified
on every published signal. Decouples ingestion from downstream reactions.

Uses Protocol for the observer contract — no base class required, any callable
or object with on_signal_ingested() qualifies (duck typing / structural subtyping).

Usage:
    bus = SignalEventBus()
    bus.register(RemediationObserver())

    # inside ingestion:
    bus.publish(signal_dict)
"""

from __future__ import annotations

import logging
from typing import Protocol

logger = logging.getLogger(__name__)


class SignalObserver(Protocol):
    def on_signal_ingested(self, signal: dict) -> None:
        ...


class SignalEventBus:

    def __init__(self) -> None:
        self._observers: list[SignalObserver] = []

    def register(self, observer: SignalObserver) -> None:
        self._observers.append(observer)

    def deregister(self, observer: SignalObserver) -> None:
        self._observers.remove(observer)

    def publish(self, signal: dict) -> None:
        for observer in self._observers:
            try:
                observer.on_signal_ingested(signal)
            except Exception:
                logger.exception("Observer %s failed on signal %s", observer, signal.get("id"))


# ---------------------------------------------------------------------------
# Concrete observer
# ---------------------------------------------------------------------------

class RemediationObserver:
    """
    PATTERN: Observer — concrete subscriber

    Fires a remediation alert for CRITICAL signals.
    Real impl would POST to PagerDuty, publish to SNS, etc.
    """

    _CRITICAL = "CRITICAL"

    def on_signal_ingested(self, signal: dict) -> None:
        if signal.get("severity") != self._CRITICAL:
            return
        logger.warning(
            "[REMEDIATION] CRITICAL signal from %s — %s",
            signal.get("service_name"),
            signal.get("summary"),
        )
