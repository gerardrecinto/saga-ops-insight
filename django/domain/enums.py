from enum import Enum


class SignalType(str, Enum):
    BUILD_FAILURE = "BUILD_FAILURE"
    DEPLOYMENT_FAILURE = "DEPLOYMENT_FAILURE"
    LATENCY_SPIKE = "LATENCY_SPIKE"
    ERROR_RATE_SPIKE = "ERROR_RATE_SPIKE"
    SECURITY_ALERT = "SECURITY_ALERT"
    DATABASE_SATURATION = "DATABASE_SATURATION"


class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

    @property
    def weight(self) -> int:
        # OCP: adding a new severity only requires a new case here, not touching scoring logic
        weights = {
            Severity.INFO: 1,
            Severity.WARNING: 3,
            Severity.CRITICAL: 5,
        }
        return weights[self]


class RiskLevel(str, Enum):
    LOW = "LOW"
    ELEVATED = "ELEVATED"
    HIGH = "HIGH"
    SEVERE = "SEVERE"
