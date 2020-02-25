#!/usr/bin python3
import os

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del oro en la bolsa de filadelfia"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://www.kitco.com/gold-price-today-usa/')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_='table-price--body-table--overview-detail')
        valor = span.get_text()
        valor = valor.split('\n')
        ORO = float(valor[14])

        ValoresMercado.objects.create(
            tipo_mercado='I',
            precio=ORO,
            par='USD/G',
            mercado=Commodities.objects.get(abreviatura='ORO')
        ).save()

