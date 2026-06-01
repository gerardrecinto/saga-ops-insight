package dev.gerard.signalharbor.api;

import dev.gerard.signalharbor.signal.Severity;
import dev.gerard.signalharbor.signal.SignalType;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.Instant;

public record CreateSignalRequest(
        @NotBlank String serviceName,
        @NotBlank String environment,
        @NotNull SignalType signalType,
        @NotNull Severity severity,
        @NotNull Instant observedAt,
        @NotBlank @Size(max = 800) String summary
) {
}
