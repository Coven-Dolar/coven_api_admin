from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def madera():
    r = requests.get('https://markets.businessinsider.com/commodities/lumber-price/usd')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="price-section__current-value")
    lumber = round(float(span.get_text().replace(',', '.')), 2)  # USD per  board feet (pies de tabla)

    if lumber > 0:
        ValoresMercado.objects.create(
            tipo_mercado='N',
            precio=lumber,
            par='USD/FBM',
            mercado=Commodities.objects.get(abreviatura='ORO')
        ).save()
