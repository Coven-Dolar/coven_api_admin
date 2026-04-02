from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def cacao():
    url = 'https://www.investing.com/commodities/us-cocoa'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return

    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(attrs={"data-test": "instrument-price-last"})
    
    if not span:
        return

    valor_text = span.get_text().strip().replace(',', '')
    cacao_val = round(float(valor_text), 2)

    if cacao_val > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=cacao_val,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='CC')
        ).save()

        cacao_val_n = round(cacao_val * 0.00453592, 2)

        ValoresMercado(
            tipo_mercado='N',
            precio=cacao_val_n,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='CC')
        ).save()
