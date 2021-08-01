from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


def maiz():
    r = requests.get('https://markets.businessinsider.com/commodities/corn-price/usd')
    soup = BeautifulSoup(r.content, 'html.parser')
    span = soup.find(class_="price-section__current-value")

    corn = round(float(span.get_text().replace(',', '.')), 2)  # USD per Bushel

    if corn > 0:
        ValoresMercado(
            tipo_mercado='I',
            precio=corn,
            par='USD/Bu',
            mercado=Commodities.objects.get(abreviatura='MAIZ')
        ).save()
