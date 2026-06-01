package dev.gerard.signalharbor.signal;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import org.springframework.stereotype.Component;

/**
 * PATTERN: Observer — Subject / Publisher (implementation pattern)
 *
 * Maintains the subscriber list and fans out events after each ingest.
 * CopyOnWriteArrayList keeps iteration thread-safe under concurrent ingestion
 * without locking the hot path.
 *
 * Spring auto-collects all SignalObserver beans into the constructor list via
 * the List<SignalObserver> injection.
 */
@Component
public class SignalEventPublisher {

    private final List<SignalObserver> observers;

    public SignalEventPublisher(List<SignalObserver> observers) {
        this.observers = new CopyOnWriteArrayList<>(observers);
    }

    public void register(SignalObserver observer) {
        observers.add(observer);
    }

    public void deregister(SignalObserver observer) {
        observers.remove(observer);
    }

    public void publish(ServiceSignal signal) {
        for (SignalObserver observer : observers) {
            observer.onSignalIngested(signal);
        }
    }
}
