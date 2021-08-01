from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def gasolina():
    r = requests.get('https://www.indexmundi.com/es/precios-de-mercado/?mercancia=gasolina')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="dailyPrice")
    gasolina = span.get_text().replace(',', '.')

    print(gasolina)

    if gasolina > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=gasolina,
            par='USD/GAL',
            mercado=Commodities.objects.get(abreviatura='Gaso')
        ).save()
