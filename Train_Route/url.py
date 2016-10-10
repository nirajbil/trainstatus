from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_Route' #name space if we have more apps

urlpatterns = [
    url(r'trainRoute/$', views.trainRoute,name="trainRoute" ),
    url(r'^train_Route_detail/$',views.train_Route_detail),
]