package dev.gerard.signalharbor.api;

import dev.gerard.signalharbor.analytics.RiskScoringService;
import dev.gerard.signalharbor.analytics.RiskSummary;
import dev.gerard.signalharbor.signal.SignalIngestionService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1")
public class SignalController {
    private final SignalIngestionService ingestionService;
    private final RiskScoringService riskScoringService;

    public SignalController(SignalIngestionService ingestionService, RiskScoringService riskScoringService) {
        this.ingestionService = ingestionService;
        this.riskScoringService = riskScoringService;
    }

    @PostMapping("/signals")
    @ResponseStatus(HttpStatus.CREATED)
    public SignalResponse createSignal(@Valid @RequestBody CreateSignalRequest request) {
        return SignalResponse.from(ingestionService.ingest(request));
    }

    @GetMapping("/services/{serviceName}/risk-summary")
    public RiskSummary summarizeRisk(@PathVariable String serviceName) {
        return riskScoringService.summarize(serviceName);
    }
}
