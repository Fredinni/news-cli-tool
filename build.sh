#!/bin/bash

echo "===================================="
echo " GENERANDO DOCKERFILE..."
echo "===================================="

cat > Dockerfile <<EOF
FROM python:3.11-slim

WORKDIR /app

COPY requerimientos.txt .
RUN pip install --no-cache-dir -r requerimientos.txt

COPY app.py .

CMD ["python", "app.py"]
EOF

echo "✅ Dockerfile generado."

echo "===================================="
echo " CONSTRUYENDO IMAGEN DOCKER..."
echo "===================================="
docker build -t news-app .

echo "===================================="
echo " EJECUTANDO CONTENEDOR..."
echo "===================================="
docker run --rm \
  --name samplerunning \
  -e NEWS_API_KEY="${NEWS_API_KEY}" \
  -e NEWS_TOPIC="${NEWS_TOPIC:-tecnologia}" \
  news-app

echo "===================================="
echo " GUARDANDO EVIDENCIA..."
echo "===================================="
mkdir -p evidencias/docker
docker ps -a > evidencias/docker/output.txt
echo "✅ Script finalizado."