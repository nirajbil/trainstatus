from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Train_Fair_Enquiry' #name space if we have more apps

urlpatterns = [
    url(r'trainFairEnquiry/$', views.trainFairEnquiry,name="trainFairEnquiry" ),
    url(r'train_fair/$', views.train_fair),
    url(r'train_fair_detail/$', views.train_fair_detail),

]