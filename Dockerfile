FROM eclipse-temurin:17-jre-alpine

WORKDIR /app
ENV SERVER_PORT=80
COPY target/signal-harbor-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:80/actuator/health || exit 1
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
