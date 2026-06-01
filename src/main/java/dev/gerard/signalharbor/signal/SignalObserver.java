package dev.gerard.signalharbor.signal;

/**
 * PATTERN: Observer (implementation pattern)
 *
 * Subject (SignalEventPublisher) calls onSignalIngested() on each registered
 * observer after a signal is persisted. Decouples ingestion from downstream
 * reactions (alerting, remediation, audit log) — add new behaviors without
 * touching SignalIngestionService.
 */
public interface SignalObserver {

    void onSignalIngested(ServiceSignal signal);
}
