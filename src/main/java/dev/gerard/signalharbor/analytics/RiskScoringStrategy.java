package dev.gerard.signalharbor.analytics;

import dev.gerard.signalharbor.signal.ServiceSignal;
import java.util.List;

/**
 * PATTERN: Strategy (implementation pattern)
 *
 * Defines the algorithm contract for risk scoring. Callers depend on this
 * interface, not on concrete implementations — swap strategies without touching
 * RiskScoringService (OCP).
 *
 * Implementations:
 *   WeightedRiskScoringStrategy  — sum severity weights (default)
 *   SpikeDetectionScoringStrategy — amplify score when signal count spikes
 */
public interface RiskScoringStrategy {

    /**
     * Compute a numeric risk score for the given signal window.
     * Higher scores map to more severe risk levels.
     */
    int computeScore(List<ServiceSignal> signals);

    /**
     * Map a raw score to a {@link RiskLevel}.
     * Default thresholds follow the DesignGurus weighted-severity model.
     */
    default RiskLevel toLevel(int score) {
        if (score >= 15) return RiskLevel.SEVERE;
        if (score >= 9)  return RiskLevel.HIGH;
        if (score >= 4)  return RiskLevel.ELEVATED;
        return RiskLevel.LOW;
    }
}
