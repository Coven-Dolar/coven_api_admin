from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class Policy(TemplateView):
    template_name = 'web/policy.html'