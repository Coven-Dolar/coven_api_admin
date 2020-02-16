#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    # A commands must define handle()
    def handle(self, *args, **options):
        # Dow Jones Commodity Index Coffee
        r = requests.get('https://markets.ft.com/data/indices/tearsheet/summary?s=DJCIKC:DJI')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_='mod-ui-data-list__value')
        ValoresMercado(
            tipo_mercado='I',
            precio=span.get_text(),
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='C')
        ).save()