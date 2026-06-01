import pytest

from signal_harbor.domain.enums import RiskLevel, Severity
from signal_harbor.domain.risk_policy import WeightedRiskPolicy


def _signals(*severities: Severity) -> list[dict]:
    return [{"severity": s.value} for s in severities]


@pytest.fixture()
def policy() -> WeightedRiskPolicy:
    return WeightedRiskPolicy()


def test_empty_signals_is_low(policy: WeightedRiskPolicy) -> None:
    score, level = policy.compute_level([])
    assert score == 0
    assert level == RiskLevel.LOW


def test_single_info_is_low(policy: WeightedRiskPolicy) -> None:
    score, level = policy.compute_level(_signals(Severity.INFO))
    assert score == 1
    assert level == RiskLevel.LOW


def test_two_warnings_is_elevated(policy: WeightedRiskPolicy) -> None:
    # 2 * WARNING(3) = 6 → ELEVATED
    score, level = policy.compute_level(_signals(Severity.WARNING, Severity.WARNING))
    assert score == 6
    assert level == RiskLevel.ELEVATED


def test_three_warnings_is_high(policy: WeightedRiskPolicy) -> None:
    # 3 * WARNING(3) = 9 → HIGH
    score, level = policy.compute_level(
        _signals(Severity.WARNING, Severity.WARNING, Severity.WARNING)
    )
    assert score == 9
    assert level == RiskLevel.HIGH


def test_three_criticals_is_severe(policy: WeightedRiskPolicy) -> None:
    # 3 * CRITICAL(5) = 15 → SEVERE
    score, level = policy.compute_level(
        _signals(Severity.CRITICAL, Severity.CRITICAL, Severity.CRITICAL)
    )
    assert score == 15
    assert level == RiskLevel.SEVERE


def test_boundary_elevated_at_4(policy: WeightedRiskPolicy) -> None:
    # INFO(1) + WARNING(3) = 4 → ELEVATED
    score, level = policy.compute_level(_signals(Severity.INFO, Severity.WARNING))
    assert score == 4
    assert level == RiskLevel.ELEVATED


def test_boundary_high_at_9(policy: WeightedRiskPolicy) -> None:
    # CRITICAL(5) + WARNING(3) + INFO(1) = 9 → HIGH
    score, level = policy.compute_level(
        _signals(Severity.CRITICAL, Severity.WARNING, Severity.INFO)
    )
    assert score == 9
    assert level == RiskLevel.HIGH


def test_boundary_severe_at_15(policy: WeightedRiskPolicy) -> None:
    # 3 * CRITICAL(5) = 15 → SEVERE
    score, level = policy.compute_level(
        _signals(Severity.CRITICAL, Severity.CRITICAL, Severity.CRITICAL)
    )
    assert score == 15
    assert level == RiskLevel.SEVERE
