from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests

from apps.indicadores.models import ValoresMercado, Commodities


class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    def handle(self, *args, **options):
        r = requests.get('https://markets.businessinsider.com/commodities/wheat-price/usd')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="price-section__current-value")
        wheat = round(float(span.get_text().replace(',', '.')), 2)

        if wheat > 0:
            ValoresMercado(
                tipo_mercado='I',
                precio=wheat,
                par='USD/Bu',
                mercado=Commodities.objects.get(abreviatura='TRIGO')
            ).save()
