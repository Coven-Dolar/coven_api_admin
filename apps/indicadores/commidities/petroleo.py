from decimal import Decimal, InvalidOperation
from typing import Optional
import re

import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

from apps.indicadores.models import ValoresMercado, Commodities


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def _normalize_price(text: str) -> Optional[Decimal]:
    if not text:
        return None

    cleaned = text.strip().replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)", cleaned)

    if not match:
        return None

    try:
        return Decimal(match.group(1))
    except (InvalidOperation, ValueError):
        return None


def _extract_price_from_html(html: str) -> Optional[Decimal]:
    soup = BeautifulSoup(html, "html.parser")

    selectors = [
        '[data-test="instrument-price-last"]',
        '[data-test="instrument-price-last"] span',
        '.instrument-price_last__KQzyA',
        '.price',
        '.last-price',
        'fin-streamer[data-field="regularMarketPrice"]',
    ]

    for selector in selectors:
        node = soup.select_one(selector)
        if node:
            text = node.get_text(" ", strip=True)
            value = _normalize_price(text)
            if value is not None:
                return value

    return None


def _fetch_price(url: str) -> Optional[Decimal]:
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except RequestException as exc:
        print("Error consultando {}: {}".format(url, exc))
        return None

    return _extract_price_from_html(response.text)


def _save_price(abreviatura: str, precio: Decimal) -> None:
    if precio <= 0:
        return

    ValoresMercado.objects.create(
        tipo_mercado='I',
        precio=precio,
        par='USD/BARRIL',
        mercado=Commodities.objects.get(abreviatura=abreviatura),
    )


def petroleo():
    sources = {
        "WTI": [
            "https://www.investing.com/commodities/crude-oil",
            "https://www.marketwatch.com/investing/future/cl.1",
        ],
        "BRENT": [
            "https://www.investing.com/commodities/brent-oil",
            "https://www.marketwatch.com/investing/future/bz.1",
        ],
    }

    for abreviatura, urls in sources.items():
        price = None

        for url in urls:
            price = _fetch_price(url)
            if price is not None:
                print("{} encontrado en {}: {}".format(abreviatura, url, price))
                break

        if price is None:
            print("No fue posible obtener {}".format(abreviatura))
            continue

        _save_price(abreviatura, price)
        