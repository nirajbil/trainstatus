from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_Between_Station' #name space if we have more apps

urlpatterns = [
    url(r'trainBetweenStation/$', views.trainBetweenStation,name="trainBetweenStation" ),

]