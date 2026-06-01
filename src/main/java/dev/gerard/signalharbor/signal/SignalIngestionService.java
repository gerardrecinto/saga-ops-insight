package dev.gerard.signalharbor.signal;

import dev.gerard.signalharbor.api.CreateSignalRequest;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * PATTERN: Observer — Subject usage (implementation pattern)
 *
 * After persisting, delegates to SignalEventPublisher to notify all registered
 * SignalObserver beans. Ingestion logic stays unchanged regardless of how many
 * downstream observers exist.
 */
@Service
public class SignalIngestionService {
    private final ServiceSignalRepository signalRepository;
    private final SignalEventPublisher eventPublisher;
    private final Counter signalsAccepted;

    public SignalIngestionService(
            ServiceSignalRepository signalRepository,
            SignalEventPublisher eventPublisher,
            MeterRegistry meterRegistry) {
        this.signalRepository = signalRepository;
        this.eventPublisher = eventPublisher;
        this.signalsAccepted = Counter.builder("signal-harbor.signals.accepted")
                .description("Signals accepted by the ingestion endpoint")
                .register(meterRegistry);
    }

    @Transactional
    @CacheEvict(value = "riskSummaries", key = "#request.serviceName().toLowerCase()")
    public ServiceSignal ingest(CreateSignalRequest request) {
        ServiceSignal saved = signalRepository.save(new ServiceSignal(
                request.serviceName(),
                request.environment(),
                request.signalType(),
                request.severity(),
                request.observedAt(),
                request.summary()
        ));
        signalsAccepted.increment();
        eventPublisher.publish(saved);
        return saved;
    }
}
