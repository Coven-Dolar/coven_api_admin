#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


class Command(BaseCommand):
    help = "Obtiene el valor de la madera"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://markets.businessinsider.com/commodities/lumber-price/usd')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="price-section__current-value")
        lumber = round(float(span.get_text().replace(',', '.')), 2) # USD per  board feet (pies de tabla)
        print(lumber)