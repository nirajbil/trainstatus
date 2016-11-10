from django.conf.urls import url
from . import views

from django.views.generic.base import TemplateView

app_name  = 'Database' #name space if we have more apps

urlpatterns = [


    url(r'Database/', views.Database, name='Database'),
    url(r'pnr/', views.pnr, name='pnr'),

]