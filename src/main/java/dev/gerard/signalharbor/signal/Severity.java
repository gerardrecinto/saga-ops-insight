package dev.gerard.signalharbor.signal;

public enum Severity {
    LOW(1),
    MEDIUM(2),
    HIGH(3),
    CRITICAL(5);

    private final int weight;

    Severity(int weight) {
        this.weight = weight;
    }

    public int weight() {
        return weight;
    }
}
