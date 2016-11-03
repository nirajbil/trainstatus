from django.conf import settings

from django.core.urlresolvers import reverse
import urllib
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout
#if not settings.configured:
 #   settings.configure()

from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from django.http import HttpResponse
import json

from datetime import timedelta
from datetime import datetime
import time

from exception_handler import log_exception
from django.db.models import Q
from pnrapi import pnrapi
from pnr_utils import get_pnr_status, caluclate_timedelta, get_pnr_status_Niraj, send_Email,get_pnr_status_for_alert_Niraj
from .tasks import send_pnr_notification
from .models import PNRNotification, RecentPNR, UserProfile, API_Key
from django.shortcuts import render, get_object_or_404



def ReadDataBase(request):
    context = {}
    list = []
    print "ReadDataBase request.user=%s" %request.user
    if request.user.is_authenticated:
        username = get_object_or_404(UserProfile, user=request.user)
        print "ReadDataBase username=%s" %username

        all_pnr_db = RecentPNR.objects.filter(userprofile=username)
        print "all_pnr_db=%s" %all_pnr_db

        for db in all_pnr_db:
            nowDate = datetime.now().date()
            dataBaseDate = datetime.strptime(db.DateOfJourney, '%d-%m-%Y').date()

            if dataBaseDate >= nowDate:
                list.append({'RecentPnrNo': db.RecentPnrNo,
                              'Srcdest': db.Srcdest,
                              'DateOfJourney': db.DateOfJourney,
                              })
                print "True"
            else:
                RecentPNR.objects.filter(RecentPnrNo=db.RecentPnrNo).delete()
                print "False"

        context['all_pnr_db'] = list
        return HttpResponse(json.dumps(context), content_type = "application/json")

    return HttpResponse(json.dumps(context), content_type = "application/json")


def index(request):
    print "== index =="
    context = {}
    template_name = 'userpanal/index.html'
    context['info_page'] = "index"
    return render(request,template_name, context)


def login_cancelled(request):
    template_name = 'userpanal/index.html'
    context = {}
    return render(request,template_name, context)

def home(request):
    template_name = 'userpanal/home.html'
    context = {}
    return render(request,template_name, context)

"""
def pnr_status(request):
    template_name = 'userpanal/pnr.html'
    context = {}
    if request.method == 'POST':
        print "pnr_status(request):"
        pnr_no = request.POST.get('pnrno')
        print "pnr_no=%s" %pnr_no
        return render(request,template_name, context)
"""


def pnr_status(request):
    print "get_pnr_status(request):"
    template_name = 'userpanal/pnr.html'
    context = {}
    if request.method == 'POST':
        pnr_no = request.POST.get('pnrno')
        print "pnr_no=%s" %pnr_no

        Error_Flag, context = get_pnr_status_Niraj(pnr_no)

        if request.user.is_authenticated:
            userprofile = get_object_or_404(UserProfile, user=request.user)
            print "request.user=%s" %userprofile

            all_pnr_db = RecentPNR.objects.filter(userprofile=userprofile)
            pnr_in_database = False

            for db in all_pnr_db:
                if db.RecentPnrNo == context['pnr']:
                    pnr_in_database = True
                    break

            if context['response_code'] == 200:
                #if(RecentPNR.objects.filter(Q(RecentPnrNo__contains=context['pnr']))):
                if pnr_in_database == True:
                    print "== PNR %s in data base == " %pnr_no
                    pass
                else:
                    print "== user is online, add pnr in data base ===== "
                    Recentpnr = RecentPNR()
                    Recentpnr.RecentPnrNo = context['pnr']
                    Recentpnr.Srcdest = context['boarding_point']['code'] + '->' + context['reservation_upto']['code']
                    Recentpnr.DateOfJourney = context['doj']
                    Recentpnr.userprofile = userprofile
                    Recentpnr.save()


        #if Error_Flag == False:
            #return render(request,'userpanal/pnr_status.html', context)
        return HttpResponse(json.dumps(context), content_type = "application/json")
        #else:
            #context = {'Error':'Error in Getting PRN status'}##
        #    print "=== Return from else part with response_code=%d" %context['response_code']
        #    return render(request,'userpanal/pnr_status.html', context)

    context['info_page'] = "pnr_status"
    return render(request,template_name, context)

def database_pnr(request ):
    context = {}
    if request.method == 'POST':
        database_Pnr = request.POST.get('database_Pnr')
        print "database_Pnr=%s" %database_Pnr

        Error_Flag, context = get_pnr_status_Niraj(database_Pnr)
        return HttpResponse(json.dumps(context), content_type = "application/json")


def pnrNotification(request):
    template_name = 'userpanal/pnrNotification.html'
    context = {}
    if request.method == "POST":
        pnr_no = request.POST.get('pnrno')
        notification_type = request.POST.get('notification_type')
        notification_type_value = request.POST.get('notification_type_value')
        notification_frequency = request.POST.get('notification_frequency')
        notification_frequency_value = request.POST.get('notification_frequency_value')

        print "pnr_no=%s" %pnr_no
        print "notification_type=%s" %notification_type
        print "notification_type_value=%s" %notification_type_value
        print "notification_frequency=%s" %notification_frequency
        print "notification_frequency_value=%s" %notification_frequency_value
        timenow = datetime.datetime.now()
        print "timenow=%s" %timenow

        print "next_schedule_time__lte=%s " %(datetime.datetime.now()+timedelta(minutes=5))

        next_schedule_time =  timenow + caluclate_timedelta(notification_frequency,notification_frequency_value)
        print "next_schedule_time=%s" %next_schedule_time

        #pnr_notifications=PNRNotification.objects.filter(next_schedule_time__lte=datetime.datetime.now()+next_schedule_time)
        #print "pnr_notifications.next_schedule_time=%s " %pnr_notifications.next_schedule_time


        """
        send_Email(
            message=u'this is test msg',
            subject='www.trainstatusonline.in Error!',
            to_addr='niraj.bilaimare@gmail.com'
        )
        """

        pnr_no = pnr_no[:10]
        try:
            pnr_notify = PNRNotification.objects.get(pnr_no=pnr_no)
            pnr_notify.notification_type = notification_type
            pnr_notify.notification_type_value = notification_type_value
            pnr_notify.notification_frequency = notification_frequency
            pnr_notify.notification_frequency_value = notification_frequency_value
            pnr_notify.next_schedule_time = next_schedule_time
            pnr_notify.save()
            print "--- PNR Data Saved ---- "
        except PNRNotification.DoesNotExist:
            print "--- PNRNotification.DoesNotExist ---- "
            pnr_notify = PNRNotification.objects.create( pnr_no=pnr_no, notification_type=notification_type,
                notification_type_value=notification_type_value, notification_frequency=notification_frequency,
                notification_frequency_value=notification_frequency_value, next_schedule_time=next_schedule_time )

        #pnr_status = get_pnr_status(pnr_notify)
        pnr_status = get_pnr_status_for_alert_Niraj(pnr_notify)
        if not pnr_status.get('error'):
            send_pnr_notification(pnr_notify=pnr_notify, pnr_status_dict=pnr_status)
        return render(request, 'userpanal/pnrNotificationStatus.html', pnr_status)
    else:
        #return HttpResponseRedirect('/')
        return render(request,template_name, context)

    return render(request,template_name, context)


def stop_notifications(request):
    pnr_no = request.GET.get('pnrno')
    if pnr_no:
        try:
            pnr_notify = PNRNotification.objects.get(pnr_no=pnr_no)
            pnr_notify.delete()
            return render(request, 'userpanal/stop_notifications.html', {'message':'Successfully Unsubscribed from www.trainstatusonline.in notifications! \n PNR Number Removed From Data Base'})
        except:
            return render(request, 'userpanal/stop_notifications.html', {'message': 'No such PNR number!'})
    else:
        return render(request, 'userpanal/stop_notifications.html')


#http://pypnrstatus.in/stop_notifications/?pnrno=4742301143