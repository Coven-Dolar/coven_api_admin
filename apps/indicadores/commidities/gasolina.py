from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def gasolina():
    url = 'https://www.investing.com/commodities/gasoline-rbob'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            return

        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(attrs={"data-test": "instrument-price-last"})
        
        if not span:
            return

        valor_text = span.get_text().strip().replace(',', '')
        gasolina_val = round(float(valor_text), 2)

        if gasolina_val > 0:
            ValoresMercado(
                tipo_mercado='I',
                precio=gasolina_val,
                par='USD/GAL',
                mercado=Commodities.objects.get(abreviatura='Gaso')
            ).save()
    except Exception as e:
        print(f"Error scraping Gasoline from Investing: {e}")
