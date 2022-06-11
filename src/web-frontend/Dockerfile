FROM openjdk:11-jre-slim

WORKDIR /usr/local/runtime
RUN apt update
RUN apt install -y maven 

COPY . .

RUN mvn clean && mvn package

EXPOSE 8080

ENTRYPOINT ["java"]
CMD ["-jar", "myweb-1.0.0.jar"]
