from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from signal_harbor.adapters.postgres import PostgresSignalRepository, build_session_factory
from signal_harbor.adapters.redis_cache import RedisCache
from signal_harbor.api.router import router
from signal_harbor.config import Settings
from signal_harbor.domain.risk_policy import WeightedRiskPolicy
from signal_harbor.services.ingestion import SignalIngestionService
from signal_harbor.services.risk import RiskScoringService


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # DIP: concrete adapters are composed here at the application boundary only
    settings = Settings()
    session_factory = build_session_factory(settings.database_url)
    repo = PostgresSignalRepository(session_factory)
    cache = RedisCache(settings.redis_url)
    policy = WeightedRiskPolicy()

    # OCP: swapping WeightedRiskPolicy for a new policy requires changing only this line
    app.state.api_key = settings.api_key
    app.state.ingestion_service = SignalIngestionService(writer=repo, cache=cache)
    app.state.risk_service = RiskScoringService(
        reader=repo, cache=cache, policy=policy, settings=settings
    )
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Signal Harbor", version="0.1.0", lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
