from apps.indicadores.commidities import dolar_euro_ve, oro_nacional
from celery import shared_task

from apps.indicadores.commidities.btc import btc
from apps.indicadores.commidities.cacao import cacao
from apps.indicadores.commidities.cafe import cafe
from apps.indicadores.commidities.carbon import carbon
from apps.indicadores.commidities.cobre import cobre
from apps.indicadores.commidities.gasolina import gasolina
from apps.indicadores.commidities.madera import madera
from apps.indicadores.commidities.maiz import maiz
from apps.indicadores.commidities.oro import oro
from apps.indicadores.commidities.petroleo import petroleo
from apps.indicadores.commidities.trigo import trigo


@shared_task(name="btc")
def hanlde_btc():
    btc()


@shared_task(name="cacao")
def hanlde_cacao():
    cacao()


@shared_task(name="cafe")
def hanlde_cafe():
    cafe()


@shared_task(name="carbon")
def hanlde_carbon():
    carbon()


@shared_task(name="gasolina")
def hanlde_gasolina():
    gasolina()


@shared_task(name="madera")
def hanlde_madera():
    madera()


@shared_task(name="maiz")
def hanlde_maiz():
    maiz()


@shared_task(name="dolar_euro_ve")
def hanlde_dolar_euro_ve():
    dolar_euro_ve()


@shared_task(name="oro")
def hanlde_oro():
    oro()


@shared_task(name="oro_nacional")
def hanlde_oro_nacional():
    oro_nacional()


@shared_task(name="petroleo")
def hanlde_petroleo():
    petroleo()


# @shared_task(name="ptr")
# def hanlde_ptr():
#     ptr()


@shared_task(name="trigo")
def hanlde_trigor():
    trigo()


@shared_task(name="cobre")
def hanlde_cobre():
    cobre()