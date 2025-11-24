FROM python:3.10-slim
WORKDIR /app
COPY fastapi_app/requirements.txt .
RUN pip install --no-cache-dir -r fastapi_app/requirements.txt
COPY fastapi_app/ .
COPY database.py .
ENV MLFLOW_TRACKING_URI=http://mlflow_server:5000
EXPOSE 8000
CMD ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# multiple instances?