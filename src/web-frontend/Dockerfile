FROM maven:3.8.5-openjdk-11-slim AS builder

WORKDIR /usr/local/runtime

COPY src src
COPY pom.xml pom.xml

RUN mvn -f pom.xml clean package

FROM openjdk:11-jre-slim

WORKDIR /usr/local/runtime

COPY --from=builder /usr/local/runtime/target/myweb-1.0.0.jar application.jar

EXPOSE 8080

ENTRYPOINT ["java"]
CMD ["-jar", "application.jar"]