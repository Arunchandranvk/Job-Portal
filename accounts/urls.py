from django.urls import path
from .views import *

urlpatterns = [
    path('cyberpark-companies/',CyberparkCompaniesView.as_view(),name='cyber-comp')
]