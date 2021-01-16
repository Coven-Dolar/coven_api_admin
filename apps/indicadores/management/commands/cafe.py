#!/usr/bin python3
import decimal
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    # A commands must define handle()
    def handle(self, *args, **options):
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
