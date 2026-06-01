"""
PATTERN: Strategy (Python implementation)

RiskPolicy is the abstract strategy. Concrete policies define the scoring
algorithm; callers never see the implementation.

OCP: new policies extend RiskPolicy — existing service code is unchanged.
"""

from abc import ABC, abstractmethod

from signal_harbor.domain.enums import RiskLevel, Severity


def _score_to_level(score: int) -> RiskLevel:
    if score >= 15:
        return RiskLevel.SEVERE
    if score >= 9:
        return RiskLevel.HIGH
    if score >= 4:
        return RiskLevel.ELEVATED
    return RiskLevel.LOW


class RiskPolicy(ABC):
    # OCP: callers depend on this abstract base — new policies extend, never modify this contract
    @abstractmethod
    def compute_level(self, signals: list[dict]) -> tuple[int, RiskLevel]:
        """Return (score, RiskLevel) given a list of signal dicts with a 'severity' key."""


class WeightedRiskPolicy(RiskPolicy):
    # SRP: only knows how to translate severity weights into a risk level
    def compute_level(self, signals: list[dict]) -> tuple[int, RiskLevel]:
        score = sum(Severity(s["severity"]).weight for s in signals)
        return score, _score_to_level(score)


class SpikeDetectionPolicy(RiskPolicy):
    """
    PATTERN: Strategy — alternate concrete implementation

    Amplifies the base weighted score when signal count exceeds spike_threshold.
    Models burst-of-noise incidents where many LOW signals indicate a real outage.

    score = base * (1 + spike_factor * max(0, count - spike_threshold))
    """

    def __init__(self, spike_threshold: int = 10, spike_factor: float = 0.5) -> None:
        self._spike_threshold = spike_threshold
        self._spike_factor = spike_factor

    def compute_level(self, signals: list[dict]) -> tuple[int, RiskLevel]:
        base = sum(Severity(s["severity"]).weight for s in signals)
        excess = max(0, len(signals) - self._spike_threshold)
        score = int(base * (1 + self._spike_factor * excess))
        return score, _score_to_level(score)
