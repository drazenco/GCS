FROM python:3.11-slim
WORKDIR /app
COPY server/python_fastapi/requirements.txt server/python_fastapi/requirements.txt
RUN pip install --no-cache-dir -r server/python_fastapi/requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn","server.python_fastapi.app:app","--host","0.0.0.0","--port","8000"]
