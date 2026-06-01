package dev.gerard.signalharbor.remediation;

import dev.gerard.signalharbor.analytics.RiskLevel;
import dev.gerard.signalharbor.signal.SignalType;
import java.time.Instant;
import java.util.Objects;

/**
 * PATTERN: Builder (implementation pattern)
 *
 * Alert has many optional fields and no valid no-arg constructor, making
 * telescoping constructors ugly and fragile. The inner Builder enforces required
 * fields at compile time and lets callers set optional ones fluently.
 *
 * Immutability: all fields are final; setters do not exist on Alert itself.
 *
 * Usage:
 *   Alert alert = new Alert.Builder("payment-service", RiskLevel.SEVERE)
 *       .triggeredAt(Instant.now())
 *       .signalType(SignalType.ERROR_RATE)
 *       .runbook("https://wiki/payment-sla")
 *       .oncallTeam("payments-oncall")
 *       .build();
 */
public final class Alert {

    private final String serviceName;
    private final RiskLevel riskLevel;
    private final Instant triggeredAt;
    private final SignalType signalType;
    private final String runbook;
    private final String oncallTeam;
    private final String message;
    private final boolean pagerDutyEnabled;

    private Alert(Builder builder) {
        this.serviceName = builder.serviceName;
        this.riskLevel = builder.riskLevel;
        this.triggeredAt = builder.triggeredAt;
        this.signalType = builder.signalType;
        this.runbook = builder.runbook;
        this.oncallTeam = builder.oncallTeam;
        this.message = builder.message;
        this.pagerDutyEnabled = builder.pagerDutyEnabled;
    }

    public String getServiceName()      { return serviceName; }
    public RiskLevel getRiskLevel()     { return riskLevel; }
    public Instant getTriggeredAt()     { return triggeredAt; }
    public SignalType getSignalType()   { return signalType; }
    public String getRunbook()          { return runbook; }
    public String getOncallTeam()       { return oncallTeam; }
    public String getMessage()          { return message; }
    public boolean isPagerDutyEnabled() { return pagerDutyEnabled; }

    @Override
    public String toString() {
        return "Alert{service=" + serviceName
                + ", level=" + riskLevel
                + ", at=" + triggeredAt
                + ", team=" + oncallTeam + "}";
    }

    // -------------------------------------------------------------------------
    // Builder
    // -------------------------------------------------------------------------

    public static final class Builder {

        // required
        private final String serviceName;
        private final RiskLevel riskLevel;

        // optional — sensible defaults
        private Instant triggeredAt = Instant.now();
        private SignalType signalType;
        private String runbook;
        private String oncallTeam;
        private String message;
        private boolean pagerDutyEnabled = false;

        public Builder(String serviceName, RiskLevel riskLevel) {
            this.serviceName = Objects.requireNonNull(serviceName, "serviceName required");
            this.riskLevel = Objects.requireNonNull(riskLevel, "riskLevel required");
        }

        public Builder triggeredAt(Instant triggeredAt) {
            this.triggeredAt = triggeredAt;
            return this;
        }

        public Builder signalType(SignalType signalType) {
            this.signalType = signalType;
            return this;
        }

        public Builder runbook(String runbook) {
            this.runbook = runbook;
            return this;
        }

        public Builder oncallTeam(String oncallTeam) {
            this.oncallTeam = oncallTeam;
            return this;
        }

        public Builder message(String message) {
            this.message = message;
            return this;
        }

        public Builder pagerDutyEnabled(boolean enabled) {
            this.pagerDutyEnabled = enabled;
            return this;
        }

        public Alert build() {
            return new Alert(this);
        }
    }
}
