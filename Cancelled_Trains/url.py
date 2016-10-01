from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Cancelled_Trains' #name space if we have more apps

urlpatterns = [
    url(r'cancelledTrains/$', views.cancelledTrains,name="cancelledTrains" ),

]