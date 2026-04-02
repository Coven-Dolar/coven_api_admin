from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def cafe():
    url = 'https://www.investing.com/commodities/us-coffee-c'
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

    coffe_text = span.get_text().strip().replace(',', '')
    coffe = round(float(coffe_text), 2)

    if coffe > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=coffe,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()

        coffe_n = round(coffe * 0.00453592, 2)

        ValoresMercado(
            tipo_mercado='N',
            precio=coffe_n,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()
