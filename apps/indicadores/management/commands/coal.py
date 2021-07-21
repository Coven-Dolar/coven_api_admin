#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests


class Command(BaseCommand):
    help = "Obtiene el valor del Carbon"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://markets.businessinsider.com/commodities/coal-price/usd')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="price-section__current-value")
        # coal = round(float(span.get_text().replace(',', '.')) / 1000, 2)
        coal = round(float(span.get_text().replace(',', '.')), 2)
        print(coal)
