from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class Policy(TemplateView):
    template_name = 'web/policy.html'
