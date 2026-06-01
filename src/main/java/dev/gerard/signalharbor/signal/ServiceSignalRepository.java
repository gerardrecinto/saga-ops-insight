package dev.gerard.signalharbor.signal;

import java.time.Instant;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ServiceSignalRepository extends JpaRepository<ServiceSignal, Long> {
    List<ServiceSignal> findByServiceNameIgnoreCaseAndObservedAtAfter(String serviceName, Instant observedAfter);
}
