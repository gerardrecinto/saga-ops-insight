package dev.gerard.signalharbor.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "signal-harbor")
public record SignalHarborProperties(String apiKey, int riskLookbackHours) {
}
