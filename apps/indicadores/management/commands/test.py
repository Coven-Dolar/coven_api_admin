from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Obtiene el valor del cafe"

    def handle(self, *args, **options):
        r = requests.get('https://markets.businessinsider.com/commodities/wheat-price/usd')
        soup = BeautifulSoup(r.content, 'html.parser')
        span = soup.find(class_="price-section__current-value")
        wheat = round(float(span.get_text().replace(',', '.')), 2)
        logger.debug('Precio del trigo ' + str(wheat))

        # r = requests.get('https://www.tridge.com/intelligences/shrimp-prawn')
        # soup = BeautifulSoup(r.content, 'html.parser')
        # print(soup)
        # span = soup.find(class_="priceValue___11gHJ")
        # btc = span.get_text().strip().replace(',', '').replace('$', '')
