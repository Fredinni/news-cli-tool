FROM python:3.11-slim

WORKDIR /app

COPY Requerimientos.txt .
RUN pip install --no-cache-dir -r Requerimientos.txt

COPY app.py .

CMD ["python", "app.py"]
