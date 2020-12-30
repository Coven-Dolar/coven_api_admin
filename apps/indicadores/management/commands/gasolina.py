#!/usr/bin python3

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor de la gasolina internacional"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://www.indexmundi.com/es/precios-de-mercado/?mercancia=gasolina')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="dailyPrice")
        gasolina = span.get_text().replace(',', '.')

        print(gasolina)
