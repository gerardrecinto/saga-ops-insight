package dev.gerard.signalharbor.api;

import dev.gerard.signalharbor.signal.ServiceSignal;
import dev.gerard.signalharbor.signal.Severity;
import dev.gerard.signalharbor.signal.SignalType;
import java.time.Instant;

public record SignalResponse(
        Long id,
        String serviceName,
        String environment,
        SignalType signalType,
        Severity severity,
        Instant observedAt,
        String summary
) {
    public static SignalResponse from(ServiceSignal signal) {
        return new SignalResponse(
                signal.getId(),
                signal.getServiceName(),
                signal.getEnvironment(),
                signal.getSignalType(),
                signal.getSeverity(),
                signal.getObservedAt(),
                signal.getSummary()
        );
    }
}
