from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

class CyberparkCompaniesView(TemplateView):
    template_name = 'cyberpark_companies.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()

        # Modify URLs to ensure they start with 'http://'
        for company in companies:
            if not company.website.startswith(('http://', 'https://')):
                company.website = 'http://' + company.website

        context['companies'] = companies
        return context
 