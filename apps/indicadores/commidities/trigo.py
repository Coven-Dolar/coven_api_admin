import logging
import sys

from bs4 import BeautifulSoup
from apps.indicadores.models import ValoresMercado, Commodities
import requests

logger = logging.getLogger(__name__)


def trigo():
    try:
        r = requests.get('https://markets.businessinsider.com/commodities/wheat-price/usd')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="price-section__current-value")
        # wheat = round(float(span.get_text().replace(',', '.')) / 1000, 2)
        wheat = round(float(span.get_text().replace(',', '.')), 2)
        logger.debug('Precio del trigo ' + str(wheat))
        if wheat > 0:
            ValoresMercado(
                tipo_mercado='I',
                precio=wheat,
                par='USD/Bu',
                mercado=Commodities.objects.get(abreviatura='TRIGO')
            ).save()

    except:
        logger.error(sys.exc_info()[0])
