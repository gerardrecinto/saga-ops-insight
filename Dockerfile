FROM eclipse-temurin:17-jre-alpine

WORKDIR /app
ENV SERVER_PORT=80
COPY target/signal-harbor-0.0.1-SNAPSHOT.jar app.jar

EXPOSE 80
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
