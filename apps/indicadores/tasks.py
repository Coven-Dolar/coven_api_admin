from celery import shared_task

from apps.indicadores.commidities.btc import btc
from apps.indicadores.commidities.cacao import cacao
from apps.indicadores.commidities.cafe import cafe
from apps.indicadores.commidities.carbon import carbon
from apps.indicadores.commidities.gasolina import gasolina
from apps.indicadores.commidities.madera import madera
from apps.indicadores.commidities.maiz import maiz
from apps.indicadores.commidities.monitor_dolar import monitor_dolar
from apps.indicadores.commidities.oro import oro
from apps.indicadores.commidities.oro_nacional import oro_nacional
from apps.indicadores.commidities.petroleo import petroleo
from apps.indicadores.commidities.ptr import ptr
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


@shared_task(name="monitor_dolar")
def hanlde_monitor_dolar():
    monitor_dolar()


@shared_task(name="oro")
def hanlde_oro():
    oro()


@shared_task(name="oro_nacional")
def hanlde_oro_nacional():
    oro_nacional()


@shared_task(name="petroleo")
def hanlde_petroleo():
    petroleo()


@shared_task(name="ptr")
def hanlde_ptr():
    ptr()


@shared_task(name="trigo")
def hanlde_trigor():
    trigo()
