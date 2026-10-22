FROM python:3.13-alpine
WORKDIR /app
COPY server.py ./
RUN chmod 0444 /app/server.py
USER 10001:10001
EXPOSE 5000
CMD ["python3", "-u", "/app/server.py"]
