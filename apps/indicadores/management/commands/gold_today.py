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
       r = requests.get('https://s3.amazonaws.com/dolartoday/data.json')
       resp = r.json()
       ORO = resp['GOLD']['rate']
       ORO = round(ORO / 28.3495,2)
       ValoresMercado.objects.create(
            tipo_mercado='N',
            precio=ORO,
            par='USD/G',
            mercado=Commodities.objects.get(abreviatura='ORO')
       ).save()

