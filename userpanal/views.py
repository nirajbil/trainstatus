from django.conf import settings

#from settings import RailwayAPI_APIKEY
#if not settings.configured:
 #   settings.configure()

from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from django.http import HttpResponse
import json

from datetime import timedelta
from exception_handler import log_exception

from pnrapi import pnrapi
from pnr_utils import get_pnr_status, caluclate_timedelta, get_pnr_status_Niraj, send_Email,get_pnr_status_for_alert_Niraj
from .tasks import send_pnr_notification
from .models import PNRNotification

RailwayAPI_APIKEY = "joymo1655"
#RailwayAPI_APIKEY = getattr(settings, 'RailwayAPI_APIKEY', '')





def index(request):
    template_name = 'userpanal/index.html'
    context = {'request': request,'user': request.user}
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
    if request.method == 'POST':
        url_pnr = "http://api.railwayapi.com/pnr_status/pnr/"
        print "1url_pnr=%s " %url_pnr
        print "RailwayAPI_APIKEY=%s" %str(RailwayAPI_APIKEY)

        pnr_no = request.POST.get('pnrno')
        url_pnr = url_pnr + pnr_no + '/apikey/' #+ RailwayAPI_APIKEY #+ '/'
        url_pnr = url_pnr + RailwayAPI_APIKEY + '/'

        print "pnr_no=%s" %pnr_no
        print "url_pnr=%s " %url_pnr

        Error_Flag, context = get_pnr_status_Niraj(url_pnr)
        #if Error_Flag == False:
            #return render(request,'userpanal/pnr_status.html', context)
        return HttpResponse(json.dumps(context), content_type = "application/json")
        #else:
            #context = {'Error':'Error in Getting PRN status'}##
        #    print "=== Return from else part with response_code=%d" %context['response_code']
        #    return render(request,'userpanal/pnr_status.html', context)
















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