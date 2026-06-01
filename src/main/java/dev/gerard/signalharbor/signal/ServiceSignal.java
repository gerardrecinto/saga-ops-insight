package dev.gerard.signalharbor.signal;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "service_signals")
public class ServiceSignal {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String serviceName;

    @Column(nullable = false)
    private String environment;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private SignalType signalType;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Severity severity;

    @Column(nullable = false)
    private Instant observedAt;

    @Column(nullable = false, length = 800)
    private String summary;

    protected ServiceSignal() {
    }

    public ServiceSignal(
            String serviceName,
            String environment,
            SignalType signalType,
            Severity severity,
            Instant observedAt,
            String summary
    ) {
        this.serviceName = serviceName;
        this.environment = environment;
        this.signalType = signalType;
        this.severity = severity;
        this.observedAt = observedAt;
        this.summary = summary;
    }

    public Long getId() {
        return id;
    }

    public String getServiceName() {
        return serviceName;
    }

    public String getEnvironment() {
        return environment;
    }

    public SignalType getSignalType() {
        return signalType;
    }

    public Severity getSeverity() {
        return severity;
    }

    public Instant getObservedAt() {
        return observedAt;
    }

    public String getSummary() {
        return summary;
    }
}
