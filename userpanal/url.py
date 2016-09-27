from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'userpanal' #name space if we have more apps

urlpatterns = [

    url(r'^$', views.index,name="index" ),
    url(r'home/$', views.home,name="home" ),
    url(r'pnr/$', views.pnr_status,name="pnr_status" ),
    url(r'pnrNotification/$', views.pnrNotification,name="pnrNotification" ),
]