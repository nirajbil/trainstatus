from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_Between_Stations' #name space if we have more apps

urlpatterns = [
    url(r'trainBetweenStations/$', views.trainBetweenStations,name="trainBetweenStations"),
    url(r'^train_between/$',views.train_between),
]