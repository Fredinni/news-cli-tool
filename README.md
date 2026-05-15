# 📰 News CLI Tool

## Stakeholder
Periodista o analista de medios que necesita monitorear
titulares actuales desde la terminal, sin abrir el navegador.

## Problema / Solución
Seguir noticias de un tema específico manualmente es lento.
Esta herramienta consulta NewsAPI y entrega los 5 titulares
más recientes con fuente, fecha y resumen en segundos.

## Variables de entorno requeridas

| Variable       | Descripción                          |
|----------------|--------------------------------------|
| NEWS_API_KEY   | Tu API Key de newsapi.org            |
| NEWS_TOPIC     | Tema a buscar: "econommia"           |
| NEWS_LANGUAGE  | Idioma: "es"                         |

## Ejecución con Docker

# Construir la imagen
docker build -t news-app .

# Ejecutar
docker run \
  -e NEWS_API_KEY=tu_clave \
  -e NEWS_TOPIC=tecnología \
  -e NEWS_COUNTRY=cl \
  news-app