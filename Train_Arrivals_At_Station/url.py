from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_Arrivals_At_Station' #name space if we have more apps

urlpatterns = [
    url(r'trainArrivalsAtStation/$', views.trainArrivalsAtStation,name="trainArrivalsAtStation" ),

]