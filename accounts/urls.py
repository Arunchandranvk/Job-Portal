from django.urls import path
from .views import *

urlpatterns = [
    path('cyberpark-companies/',CyberparkCompaniesView.as_view(),name='cyber-comp'),
    path('indeed-jobs/',indeed_job_search_view,name='indeed'),
    path('technopark-jobs/',Technopark_job_search_view,name='technopark'),
    path('cyberpark-jobs/',Cyberpark_job_search_view,name='cyberpark'),
    path('infopark-jobs/',Infopark_job_search_view,name='infopark'),
]