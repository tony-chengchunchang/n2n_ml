FROM python:3.10-slim
WORKDIR /app
COPY streamlit_app/requirements.txt .
RUN pip install --no-cache-dir -r streamlit_app/requirements.txt
COPY streamlit_app/ .
ENV FASTAPI_SERVER_URL=http://fastapi:8000
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app/st_app.py"]
# does this need to run at the root?