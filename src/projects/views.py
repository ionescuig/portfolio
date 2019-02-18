from django.views.generic import TemplateView
from django.shortcuts import render


class LandingView(TemplateView):
    template_name = 'projects/underconstruction.html'
