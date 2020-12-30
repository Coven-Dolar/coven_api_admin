#!/usr/bin python3
import os

from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

class Command(BaseCommand):
    help = "Obtiene el valor del cacao"

    # A commands must define handle()
    def handle(self, *args, **options):
        r = requests.get('https://finance.yahoo.com/quote/CC%3DF?p=CC%3DF')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
        cacao = round(float(span.get_text().replace(',', '')) * 0.00453592, 2)

        ValoresMercado(
            tipo_mercado='I',
            precio=cacao,
            par='USD/QQ',
            mercado=Commodities.objects.get(abreviatura='CC')
        ).save()
