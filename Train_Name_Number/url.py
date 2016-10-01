from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_NameNumber' #name space if we have more apps

urlpatterns = [


    url(r'trainNameNumber/$', views.trainNameNumber,name="trainNameNumber" ),

]