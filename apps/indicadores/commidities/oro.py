from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests
import re


def oro():
    # Intento 1: Investing.com
    url = 'https://www.investing.com/currencies/xau-usd'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            span = soup.find(attrs={"data-test": "instrument-price-last"})
            if span:
                valor_text = span.get_text().strip().replace(',', '')
                oro_val = float(valor_text)
                if oro_val > 0:
                    ValoresMercado.objects.create(
                        tipo_mercado='I',
                        precio=oro_val,
                        par='USD/G',
                        mercado=Commodities.objects.get(abreviatura='ORO')
                    ).save()
    except Exception as e:
        print(f"Error scraping Gold from Investing: {e}")
