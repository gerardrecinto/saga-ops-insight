import pytest
from django.conf import settings
from django.test import Client

from domain.risk_policy import WeightedRiskPolicy
from services.ingestion import SignalIngestionService
from services.risk import RiskScoringService
from signals import _services as _svc
from signals._fake_cache import FakeCache
from signals.orm_adapter import DjangoSignalRepository


class _TestSettings:
    risk_lookback_hours: int = 24
    cache_ttl_seconds: int = 60


@pytest.fixture(autouse=True)
def wire_test_services(db):
    """Replace app-level services with isolated test doubles before each test."""
    cache = FakeCache()
    repo = DjangoSignalRepository()
    policy = WeightedRiskPolicy()
    test_settings = _TestSettings()

    _svc.ingestion = SignalIngestionService(writer=repo, cache=cache)
    _svc.risk = RiskScoringService(
        reader=repo,
        cache=cache,
        policy=policy,
        settings=test_settings,
    )


@pytest.fixture()
def api_client():
    return Client(HTTP_X_API_KEY=settings.SIGNAL_HARBOR_API_KEY)
