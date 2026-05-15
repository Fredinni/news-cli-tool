import os
import sys
import requests
from datetime import datetime


API_KEY  = os.getenv('NEWS_API_KEY', '0981e57bd7034b9186f569a48e82c102')
TOPIC    = os.getenv('NEWS_TOPIC', 'economia')
COUNTRY  = os.getenv('NEWS_COUNTRY', 'cl')

def get_news(topic, country, api_key):

    # Error 1: clave no configurada
    if not api_key:
        print("❌ ERROR: Variable de entorno NEWS_API_KEY no configurada.")
        sys.exit(1)

    url = "https://newsapi.org/v2/everything"
    params = {
        "q"        : topic,
        "language" : "es",
        "apiKey"   : api_key,
        "pageSize" : 5,
        "sortBy"   : "publishedAt"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        # Error 2: clave inválida o sin permisos (401)
        if response.status_code == 401:
            print("❌ ERROR 401: API Key inválida o no autorizada.")
            sys.exit(1)

        # Error 3: demasiadas solicitudes (429)
        if response.status_code == 429:
            print("❌ ERROR 429: Límite de solicitudes alcanzado. Intenta más tarde.")
            sys.exit(1)

        # Error 4: servidor caído (500)
        if response.status_code == 500:
            print("❌ ERROR 500: Error interno del servidor de NewsAPI.")
            sys.exit(1)

        # Error 5: cualquier otro código inesperado
        if response.status_code != 200:
            print(f"❌ ERROR HTTP {response.status_code}: respuesta inesperada.")
            sys.exit(1)

        data = response.json()

        # Sin resultados
        if data.get('totalResults', 0) == 0:
            print(f"⚠️  No se encontraron noticias para '{topic}' en '{country}'.")
            sys.exit(0)

        articles = data['articles']

        print("=" * 55)
        print(f"  📰  NOTICIAS SOBRE: {topic.upper()}")
        print(f"  🌎  País: {country.upper()} | {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print("=" * 55)

        for i, article in enumerate(articles, start=1):
            # ✅ Procesamiento de ≥3 campos por artículo
            titulo  = article.get('title',       'Sin título')       # campo 1
            fuente  = article.get('source', {}).get('name', 'Desconocida')  # campo 2
            fecha   = article.get('publishedAt', 'Sin fecha')        # campo 3
            desc    = article.get('description', 'Sin descripción')  # campo 4
            url_art = article.get('url',         'Sin URL')          # campo 5

            # Formatear fecha
            try:
                fecha_fmt = datetime.strptime(fecha, "%Y-%m-%dT%H:%M:%SZ")
                fecha_fmt = fecha_fmt.strftime("%d/%m/%Y %H:%M")
            except Exception:
                fecha_fmt = fecha

            print(f"\n  [{i}] {titulo}")
            print(f"       📡 Fuente  : {fuente}")
            print(f"       📅 Fecha   : {fecha_fmt}")
            print(f"       📝 Resumen : {desc[:120] if desc else 'N/A'}...")
            print(f"       🔗 URL     : {url_art}")
            print("  " + "-" * 53)

        print(f"\n  ✅ Total de resultados disponibles: {data['totalResults']}")
        print("=" * 55)

    # Error 6: timeout
    except requests.exceptions.Timeout:
        print("❌ ERROR: La solicitud tardó demasiado (Timeout).")
        sys.exit(1)

    # Error 7: sin conexión
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Sin conexión a internet. Verifica tu red.")
        sys.exit(1)

    # Error 8: respuesta malformada
    except (KeyError, ValueError) as e:
        print(f"❌ ERROR al procesar la respuesta de la API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    get_news(TOPIC, COUNTRY, API_KEY)