from django.conf.urls import url
from . import views
#from django.contrib.auth import views
from django.views.generic.base import TemplateView


app_name  = 'Seat_Availability' #name space if we have more apps

urlpatterns = [

    #url(r'^seatAvailability/$', 'Seat_Availability.views.seatAvailability' ),
    url(r'seatAvailability/$', views.seatAvailability ,name="seatAvailability" ),
    url(r'^find_train/$',views.find_train),
    url(r'^find_seat/$',views.find_seat),
]