package dev.gerard.signalharbor.analytics;

import java.time.Instant;
import java.util.Map;

public record RiskSummary(
        String serviceName,
        Instant windowStart,
        Instant windowEnd,
        int signalCount,
        int riskScore,
        RiskLevel riskLevel,
        Map<String, Long> signalsByType
) {
}
