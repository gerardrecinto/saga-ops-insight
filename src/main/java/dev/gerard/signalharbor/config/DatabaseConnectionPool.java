package dev.gerard.signalharbor.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.ArrayDeque;
import java.util.Deque;

/**
 * PATTERN: Singleton (implementation pattern)
 *
 * Guarantees exactly one pool instance per JVM. Uses double-checked locking so
 * the lock is only acquired on the first call — subsequent calls read the
 * volatile field without entering the synchronized block.
 *
 * Why volatile: without it the JVM may publish a partially-constructed object
 * to other threads between the 'new' allocation and field assignments.
 *
 * Trade-off: Spring already manages connection pools (HikariCP). This class
 * demonstrates the raw pattern for architecture reviews — in production prefer
 * Spring's DataSource injection.
 */
public final class DatabaseConnectionPool {

    private static volatile DatabaseConnectionPool instance;

    private final Deque<Connection> pool = new ArrayDeque<>();
    private final String url;
    private final String username;
    private final String password;
    private final int poolSize;

    private DatabaseConnectionPool(String url, String username, String password, int poolSize)
            throws SQLException {
        this.url = url;
        this.username = username;
        this.password = password;
        this.poolSize = poolSize;
        for (int i = 0; i < poolSize; i++) {
            pool.push(DriverManager.getConnection(url, username, password));
        }
    }

    /** Double-checked locking — thread-safe lazy init. */
    public static DatabaseConnectionPool getInstance(
            String url, String username, String password, int poolSize) throws SQLException {
        if (instance == null) {
            synchronized (DatabaseConnectionPool.class) {
                if (instance == null) {
                    instance = new DatabaseConnectionPool(url, username, password, poolSize);
                }
            }
        }
        return instance;
    }

    public synchronized Connection acquire() throws SQLException {
        if (pool.isEmpty()) {
            return DriverManager.getConnection(url, username, password);
        }
        return pool.pop();
    }

    public synchronized void release(Connection connection) {
        if (pool.size() < poolSize) {
            pool.push(connection);
        } else {
            try {
                connection.close();
            } catch (SQLException ignored) {
            }
        }
    }

    public synchronized int available() {
        return pool.size();
    }

    /** Reset for tests — never call in production. */
    static synchronized void resetForTesting() {
        instance = null;
    }
}
