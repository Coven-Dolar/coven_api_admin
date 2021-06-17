from django.urls import path
from .views import Policy

urlpatterns = [
    path('policy', Policy.as_view()),
]