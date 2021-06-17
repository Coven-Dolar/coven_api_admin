from django.urls import path

from apps.indicadores.views import MarketGraph

urlpatterns = [
    path('data/<typemarket>/<market>/', MarketGraph.as_view()),
]
