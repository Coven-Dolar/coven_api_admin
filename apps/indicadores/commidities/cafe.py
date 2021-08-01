from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def cafe():
    r = requests.get('https://www.economies.com/commodities/coffee')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="Last site-float")

    coffe = round(float(span.get_text().strip().replace(',', '')) * 0.00453592, 2)

    if coffe > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=coffe,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()
