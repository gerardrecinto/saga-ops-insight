package dev.gerard.signalharbor.analytics;

import static org.assertj.core.api.Assertions.assertThat;

import dev.gerard.signalharbor.config.SignalHarborProperties;
import dev.gerard.signalharbor.signal.ServiceSignal;
import dev.gerard.signalharbor.signal.ServiceSignalRepository;
import dev.gerard.signalharbor.signal.Severity;
import dev.gerard.signalharbor.signal.SignalType;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;

@DataJpaTest
@ActiveProfiles("test")
class RiskScoringServiceTest {
    private final ServiceSignalRepository signalRepository;

    @Autowired
    RiskScoringServiceTest(ServiceSignalRepository signalRepository) {
        this.signalRepository = signalRepository;
    }

    @Test
    void summarizesRiskWithinConfiguredLookbackWindow() {
        Instant now = Instant.parse("2026-05-31T12:00:00Z");
        signalRepository.save(new ServiceSignal(
                "automation-api",
                "prod",
                SignalType.ERROR_RATE_SPIKE,
                Severity.CRITICAL,
                now.minusSeconds(3600),
                "5xx error rate crossed alert threshold"
        ));
        signalRepository.save(new ServiceSignal(
                "automation-api",
                "prod",
                SignalType.LATENCY_SPIKE,
                Severity.HIGH,
                now.minusSeconds(7200),
                "p95 latency doubled after deploy"
        ));
        signalRepository.save(new ServiceSignal(
                "automation-api",
                "prod",
                SignalType.BUILD_FAILURE,
                Severity.CRITICAL,
                now.minusSeconds(100_000),
                "outside the lookback window"
        ));

        RiskScoringService service = new RiskScoringService(
                signalRepository,
                new SignalHarborProperties("test-api-key", 24),
                Clock.fixed(now, ZoneOffset.UTC),
                new SimpleMeterRegistry(),
                new WeightedRiskScoringStrategy()
        );

        RiskSummary summary = service.summarize("automation-api");

        assertThat(summary.signalCount()).isEqualTo(2);
        assertThat(summary.riskScore()).isEqualTo(8);
        assertThat(summary.riskLevel()).isEqualTo(RiskLevel.ELEVATED);
        assertThat(summary.signalsByType())
                .containsEntry("ERROR_RATE_SPIKE", 1L)
                .containsEntry("LATENCY_SPIKE", 1L);
    }
}
