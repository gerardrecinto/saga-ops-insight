package dev.gerard.signalharbor.api;

import static org.hamcrest.Matchers.equalTo;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class SignalControllerTest {
    private final MockMvc mockMvc;

    @Autowired
    SignalControllerTest(MockMvc mockMvc) {
        this.mockMvc = mockMvc;
    }

    @Test
    void rejectsRequestsWithoutApiKey() throws Exception {
        mockMvc.perform(get("/api/v1/services/automation-api/risk-summary"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void ingestsSignalsAndReturnsRiskSummary() throws Exception {
        mockMvc.perform(post("/api/v1/signals")
                        .header("X-API-Key", "test-api-key")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "serviceName": "automation-api",
                                  "environment": "prod",
                                  "signalType": "SECURITY_ALERT",
                                  "severity": "CRITICAL",
                                  "observedAt": "2026-05-31T12:00:00Z",
                                  "summary": "Unauthorized API-key spray detected at gateway"
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.serviceName", equalTo("automation-api")))
                .andExpect(jsonPath("$.severity", equalTo("CRITICAL")));

        mockMvc.perform(get("/api/v1/services/automation-api/risk-summary")
                        .header("X-API-Key", "test-api-key"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.signalCount", equalTo(1)))
                .andExpect(jsonPath("$.riskScore", equalTo(5)))
                .andExpect(jsonPath("$.riskLevel", equalTo("ELEVATED")));
    }
}
