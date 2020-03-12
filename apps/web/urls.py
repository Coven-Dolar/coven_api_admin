from django.urls import path

from apps.indicadores.views import Internacional, Nacional
from .views import Policy

urlpatterns = [
    path('policy', Policy.as_view()),
]