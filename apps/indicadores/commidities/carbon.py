from bs4 import BeautifulSoup
import requests

from apps.indicadores.models import ValoresMercado, Commodities


def carbon():
    r = requests.get('https://markets.businessinsider.com/commodities/coal-price/usd')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="price-section__current-value")

    carbon = round(float(span.get_text().replace(',', '.')), 2)

    if carbon > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=carbon,
            par='USD/T',
            mercado=Commodities.objects.get(abreviatura='CARBON')
        ).save()


        ValoresMercado(
            tipo_mercado='N',
            precio=round(carbon * 0.00453592, 2),
            par='USD/T',
            mercado=Commodities.objects.get(abreviatura='CARBON')
        ).save()
