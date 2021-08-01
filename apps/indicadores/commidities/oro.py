from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def oro():
    r = requests.get('https://www.kitco.com/gold-price-today-usa/')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_='table-price--body-table--overview-detail')
    valor = span.get_text()
    valor = valor.split('\n')
    ORO = float(valor[14])

    if ORO > 0:
        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=ORO,
            par='USD/G',
            mercado=Commodities.objects.get(abreviatura='ORO')
        ).save()

    r = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
    resp = r.json()
    ORO = resp['GOLD']['rate']
    ORO = round(ORO / 28.3495, 2)

    if ORO > 0:
        ValoresMercado.objects.create(
            tipo_mercado='N',
            precio=ORO,
            par='USD/G',
            mercado=Commodities.objects.get(abreviatura='ORO')
        ).save()
