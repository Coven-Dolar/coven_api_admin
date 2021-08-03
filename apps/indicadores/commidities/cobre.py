from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def cobre():
    r = requests.get('https://markets.businessinsider.com/commodities/copper-price/usd')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="price-section__current-value")
    copper = round(float(span.get_text().replace(',', '.')), 2)

    if copper > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=copper,
            par='USD/T',
            mercado=Commodities.objects.get(abreviatura='COBRE')
        ).save()
