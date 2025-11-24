FROM python:3.10-slim
WORKDIR /app
COPY worker_app/ .
COPY database.py .
CMD ["python", "worker_app/worker.py"]