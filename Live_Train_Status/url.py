from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Live_Train_Status' #name space if we have more apps

urlpatterns = [

    url(r'liveTrainStatus/$', views.liveTrainStatus,name="liveTrainStatus" ),
]