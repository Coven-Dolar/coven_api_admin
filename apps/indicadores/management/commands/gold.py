#!/usr/bin python3
import os

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.db.models import Max, Count, Subquery, OuterRef
from django.utils import timezone
from apps.indicadores.models import ValoresMercado, Commodities
from datetime import date
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

        valores = ValoresMercado.objects.filter(fecha__gte=date.today(), mercado__mercado_internacional=True)
        mess = ''
        for valor in valores:
            mess += str(valor.mercado) + ': ' + str(valor.precio) + ' ' + str(valor.par) + ' \n'

        from fcm_django.models import FCMDevice
        device = FCMDevice.objects.all().first()
        device.send_message(title="Actualización de Commodities Internacionales. ",
                            body=mess)



