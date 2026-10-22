FROM debian:trixie-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY overflow entrypoint.sh ./
RUN chmod 0555 /app/overflow /app/entrypoint.sh
USER 10001:10001
EXPOSE 5000
ENTRYPOINT ["/app/entrypoint.sh"]
