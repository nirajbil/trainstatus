from django.conf.urls import url
from . import views

from django.views.generic.base import TemplateView

app_name  = 'userpanal' #name space if we have more apps

urlpatterns = [

    url(r'^$', views.index,name="index" ),
    url(r'home/$', views.home,name="home" ),
    url(r'pnr_status/$', views.pnr_status,name="pnr_status" ),
    url(r'pnrNotification/$', views.pnrNotification,name="pnrNotification" ),
    url(r'stop_notifications/', views.stop_notifications, name='stop_notifications'),


    url(r'^database_pnr/', views.database_pnr),
    url(r'ReadDataBase/$', views.ReadDataBase),
]