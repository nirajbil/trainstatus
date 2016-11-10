"""railway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from django.contrib import admin
from userpanal.views import login_cancelled
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('userpanal.url',namespace='userpanal')),
    url(r'^', include('Train_Route.url',namespace='Train_Route')),
    url(r'^', include('Live_Train_Status.url',namespace='Live_Train_Status')),
    url(r'^', include('Seat_Availability.url',namespace='Seat_Availability')),
    url(r'^', include('Train_Between_Stations.url',namespace='Train_Between_Stations')),
    url(r'^', include('Train_Name_Number.url',namespace='Train_Name_Number')),
    url(r'^', include('Train_Fair_Enquiry.url',namespace='Train_Fair_Enquiry')),
    url(r'^', include('Train_Arrivals_At_Station.url',namespace='Train_Arrivals_At_Station')),
    url(r'^',include('Cancelled_Trains.url',namespace='Cancelled_Trains')),
    url(r'^',include('Database.url',namespace='Database')),

    url(r'^accounts/social/login/cancelled/$', login_cancelled),
    url(r'^accounts/', include('allauth.urls')),

    #url('', include('social.apps.django_app.urls', namespace='social')),
    #url('', include('django.contrib.auth.urls', namespace='auth')),
]
