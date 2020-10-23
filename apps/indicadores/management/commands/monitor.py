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
        r = requests.get('https://monitordolarvenezuela.com/')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_='box-calcmd text-center')
        valor = span.get_text()
        valor = valor.split('\n')
        print(valor)
        usd = valor[2]
        eur = valor[3]
        bcv = valor[4]
        paypal = valor[11]

        eur = float(eur.replace('Monitor Euro:', '').replace(' Bs.S', '').replace('.', '').replace(',', '.'))
        bcv = float(bcv.replace('BCV: ', '').replace(' Bs.S', '').replace('.', '').replace(',', '.'))
        usd = float(usd.replace('Monitor Dolar: ', '').replace(' Bs.S', '').replace('.', '').replace(',', '.'))
        paypal = float(paypal.replace('Paypal: ', '').replace(' Bs.S', '').replace('.', '').replace(',', '.'))

        if usd > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=usd,
                par='BS/USD',
                mercado=Commodities.objects.get(abreviatura='USD')
            ).save()

        if paypal > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=paypal,
                par='BS/USD',
                mercado=Commodities.objects.get(abreviatura='Payp')
            ).save()

        if eur > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=eur,
                par='BS/EUR',
                mercado=Commodities.objects.get(abreviatura='EUR')
            ).save()

        if bcv > 0:
            ValoresMercado.objects.create(
                tipo_mercado='N',
                precio=bcv,
                par='BS/USD',
                mercado=Commodities.objects.get(abreviatura='BCV')
            ).save()

        '''from fcm_django.models import FCMDevice
        device = FCMDevice.objects.all().first()
        device.send_message(title="Actualización de Precio.",
                            icon="https://coven.jaspesoft.com/static/imagen/icon.png",
                            body="Dolar: "+str(usd)+" \n"
                                               "Paypal "+str(paypal)+" \n"
                                                "Euro " + str(eur))'''

