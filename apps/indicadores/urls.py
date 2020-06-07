from django.urls import path

from apps.indicadores.views import Internacional, Nacional, LeyendaMercado

urlpatterns = [
    path('mercados/internacionales/', Internacional.as_view()),
    path('mercados/nacionales/', Nacional.as_view()),
    path('mercados/leyenda/<leyenda>/', LeyendaMercado.as_view()),
]