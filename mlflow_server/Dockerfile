FROM python:3.10-slim
WORKDIR /app
COPY mlflow_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["mlflow", "server", "--backend-store-uri", "sqlite:///mlflow_data/mlflow.db", "--default-artifact-root", "/app/mlflow_data/artifacts", "--host", "0.0.0.0", "--port", "5000"]