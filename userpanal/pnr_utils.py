import datetime

import requests
import urllib2
import json
from pprint import pprint

from pnrapi import pnrapi
from .exception_handler import log_exception
from .models import PNRStatus, API_Key

RailwayAPI_APIKEY = API_Key.objects.get().RailwayAPI_APIKEY#"joymo1655"

def check_if_passengers_cnf(passengers):
    for passenger in passengers:
        if passenger['seat_number'] != 'CNF':
            return False
    return True

def check_if_ticket_cancelled(passengers):
    cancel_count = 0
    total_count = len(passengers)
    for passenger in passengers:
        if passenger['seat_number'] == 'Can/Mod':
            cancel_count += 1
    if cancel_count == total_count:
        return True
    return False


def caluclate_timedelta(notification_frequency, notification_frequency_value):
    notification_frequency_value = int(notification_frequency_value)
    if notification_frequency == 'Minutes':
        timedelta = datetime.timedelta(minutes=notification_frequency_value)
    elif notification_frequency == 'Hours':
        timedelta = datetime.timedelta(hours=notification_frequency_value)
    elif notification_frequency == 'Days':
        timedelta = datetime.timedelta(days=notification_frequency_value)
    return timedelta


def schedule_notification_now(pnr_notify):
    now = datetime.datetime.now()
    timedelta = caluclate_timedelta('Minutes', 1)
    pnr_notify.next_schedule_time = now + timedelta
    pnr_notify.save()

@log_exception
def get_pnr_status(pnr_notify, delete_on_fail=True):
    pnr_no = pnr_notify.pnr_no
    p = pnrapi.PnrApi(pnr_no)

    print "In get_pnr_status resp=%s" %p.get_json()

    if not p.request():
        if delete_on_fail:
            pnr_notify.delete()

        """
        send_email(
            message=u'PNR: {} \n\n Error: {}'.format(pnr_no, p.error),
            subject='Py-PNR-Status Error!',
            to_addr='niraj.bilaimare@gmail.com'
        )
        """
        return {'error': p.error}
    resp = p.get_json()

    print "In get_pnr_status resp=%s" %resp

    def _map_passenger(passenger):
        return {
           'seat_number': passenger['current_status'],
           'status': passenger['booking_status']
        }
    passengers = [_map_passenger(key) for key in resp['passengers']]

    ticket_is_cancelled = ticket_is_confirmed = chart_prepared_for_ticket = None
    will_get_notifications = True

    if check_if_ticket_cancelled(passengers):
        ticket_is_cancelled = True
        will_get_notifications = False
    if check_if_passengers_cnf(passengers):
        ticket_is_confirmed = True
        will_get_notifications = False
    if resp['charting_status'] == 'CHART PREPARED' or resp['chart_prepared'] == 'Y':
        chart_prepared_for_ticket = True
        will_get_notifications = False


    json_dict =  {'pnr_no': pnr_no,
                  'passengers': passengers,
                  'ticket_is_cancelled': ticket_is_cancelled,
                  'ticket_is_confirmed': ticket_is_confirmed,
                  'chart_prepared_for_ticket': chart_prepared_for_ticket,
                  'will_get_notifications': will_get_notifications,
                  'pnr_notify': pnr_notify }

    pnr_status, cr = PNRStatus.objects.get_or_create(pnr_no=pnr_no)
    pnr_status.status = resp
    pnr_status.save()
    return json_dict


def get_current_status(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'Passenger %s ' % i +'<br/>' + 'Booking Status: ' + passenger['status']
        temp = temp +'<br/>'+ 'Current Status: ' + passenger['seat_number']+'<br/><br/>'
        i+=1
    return temp

def get_current_status_sms(passengers):
    temp=''
    i = 1
    for passenger in passengers:
        temp = temp+ 'P%s ' % i +'\n' + 'Book Stat.: ' + passenger['status']
        temp = temp +'\n'+ 'Curr Stat:' + passenger['seat_number']+'\n\n'
        i+=1
    return temp

"""
def send_email(message, subject, to_addr):
    print 'sending'
    requests.post('https://api.mailgun.net/v2/pypnrstatus.in/messages',
        auth=("api", "key-3du65990xbf63jlr5ihvlpir2k82jqr5"),
        data={"from": "TrainStatusOnline.in <info@TrainStatusOnline.in>",
            "to": [to_addr],
            "subject": subject,
            "html": message,
            "text": message})
    print 'sent :)'
"""
#"https://api.mailgun.net/v3/sandbox89e4eae13fb8486e805592b6d3605e83.mailgun.org/messages",
def send_Email(message, subject, to_addr):
    print 'sending'
    success = requests.post(
        "https://api.mailgun.net/v3/sandbox89e4eae13fb8486e805592b6d3605e83.mailgun.org/messages",
        auth=("api", "key-5e1158e1344872a19a4d9b1560e8b4a7"),
        data={"from": "TrainStatusOnline.in <info@TrainStatusOnline.in> ",
              "to": [to_addr],
              "subject": subject,
              "html": message,
              "text": message })

    print success
    if success == 200:
        print "+++ success ++++ "

    if success[0] == 200:
        print "+++ success[0] ++++ "

    print 'sent :)'


def send_sms(message, phone_no):
    print 'sending'
    import plivo
    p = plivo.RestAPI('MANJI0Y2YXODRMNZCZZW', 'NzEwNTQ2YTE4N2JhYzFkNGU1Yzg2ZjZlZjIyYzA0')
    plivo_number = '910123456789'
    if len(phone_no) == 10:
        phone_no = '91'+phone_no
    message_params = {
      'src':plivo_number,
      'dst':phone_no,
      'text':message,
    }
    print p.send_message(message_params)
    print 'sent :)'





# email helpers
def send_pnr_status_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    unsubscribe_link = "<a href='http://127.0.0.1:8000/stop_notifications/?pnrno=%s'>Unsubscribe (Stop Notifications)</a>"%pnr_notify.pnr_no
    message += '<br/><br/>' + unsubscribe_link
    subject = "PNR Status %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_Email(message, subject, to_addr)

def send_pnr_status_chart_prepared_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Chart Prepared for PNR %s</b> <br/><br/>' % pnr_notify.pnr_no) + message
    subject = "Chart Prepared for PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_Email(message, subject, to_addr)

def send_pnr_status_confirmed_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Ticket Confirmed for PNR %s  :)</b> <br/><br/>' % pnr_notify.pnr_no)  + message
    subject = "PNR Status Confirmed! PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_Email(message, subject, to_addr)

def send_tatkal_ticket_book_email(passengers, pnr_notify):
    pass

def send_ticket_cancelled_email(passengers, pnr_notify):
    message = get_current_status(passengers)
    message = ('<b>Your ticket with PNR %s was cancelled!</b> <br/><br/>' % pnr_notify.pnr_no) + message
    subject = "Your ticket was cancelled! PNR %s"%pnr_notify.pnr_no
    to_addr = pnr_notify.notification_type_value
    send_Email(message, subject, to_addr)

# sms helpers
def send_pnr_status_sms(passengers, pnr_notify):
    message = 'PNR %s\n'% pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    message += '\n- pypnrstatus.in'
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_pnr_status_chart_prepared_sms(passengers, pnr_notify):
    message = 'Chart prepared for PNR %s\n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_pnr_status_confirmed_sms(passengers, pnr_notify):
    message = 'Ticket CNF for PNR %s\n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)

def send_tatkal_ticket_book_sms(passengers, pnr_notify):
    pass

def send_ticket_cancelled_sms(passengers, pnr_notify):
    message = 'Ticket Cancelled for PNR %s \n' % pnr_notify.pnr_no
    message += get_current_status_sms(passengers)
    phone_no = pnr_notify.notification_type_value
    send_sms(message, phone_no)


#+++++++++++++++++++++++++++++++ Niraj Code ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

"""
    content='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> \
    <title>500 Internal Server Error</title> \
    <h1>Internal Server Error</h1> \
    <p>The server encountered an internal error and was unable to complete your request.  Either the server is overloaded or there is an error in the \
     application.</p>'
"""

def get_pnr_status_Niraj(pnrno):
    url_pnr = "http://api.railwayapi.com/pnr_status/pnr/"
    url_pnr = url_pnr + pnrno + '/apikey/' + RailwayAPI_APIKEY + '/'
    print "url_pnr=%s " %url_pnr

    request_data = {}
    context = {}

    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    #pprint(request_data)

    response_code = request_data['response_code']
    error = request_data['error']

    if response_code == 200:
        boarding_point = request_data['boarding_point']
        chart_prepared = request_data['chart_prepared']
        train_class = request_data['class']
        doj = request_data['doj']
        pnr = request_data['pnr']

        from_station = request_data['from_station']
        reservation_upto = request_data['reservation_upto']
        to_station = request_data['to_station']
        total_passengers = request_data['total_passengers']

        train_name = request_data['train_name']
        train_num = request_data['train_num']
        train_start_date = request_data['train_start_date']

        passengers = request_data['passengers']

        print "passengers=%s" %passengers
        print "boarding_point=%s" %request_data['boarding_point']
        print "boarding_point code=%s" %request_data['boarding_point']['code']
        print "boarding_point name=%s" %request_data['boarding_point']['name']
        print "response_code=%d" %request_data['response_code']

        context = {'boarding_point': boarding_point,
                   'chart_prepared': chart_prepared,
                   'train_class': train_class,
                   'doj': doj,
                   'from_station': from_station,
                   'pnr': pnr,
                   'reservation_upto': reservation_upto,
                   'to_station': to_station,
                   'total_passengers': total_passengers,
                   'train_name': train_name,
                   'train_num': train_num,
                   'train_start_date': train_start_date,
                   'passengers': passengers,
                   'response_code': response_code,
                   'error': error,
                   }
        return context

    else:
         if response_code == 404:
            Error_str = ' Error:404 \n\n Service Down / Source not responding'
         elif response_code == 410:
             Error_str=' Error:410 \n\n Flushed PNR / PNR not yet generated'
         elif response_code == 204:
             Error_str=' Error:204 \n\n Empty response. Not able to fetch required data.'
         elif response_code == 401:
            Error_str=' Error:401 \n\n Authentication Error. You passed an unknown API Key.'
         elif response_code == 403:
             Error_str=' Error:403 \n\n Quota for the day exhausted. Applicable only for FREE users.'
         elif response_code == 405:
            Error_str=' Error:405 \n\n Account Expired. Renewal was not completed on time.'
         else:
             Error_str='Some Other Error...'

         context = {
                   'response_code': response_code,
                   'error': error,
                   'Error_str': Error_str,
                   }

         print "get_pnr_status_Niraj Error in communication response_code=%d" %response_code
         return context

"""
{u'boarding_point': {u'code': u'GDR', u'name': u'GUDUR JN'},
 u'chart_prepared': u'N',
 u'class': u'SL',
 u'doj': u'25-9-2016',
 u'error': False,
 u'failure_rate': 45.352112676056336,
 u'from_station': {u'code': u'GDR', u'name': u'GUDUR JN'},
 u'passengers': [{u'booking_status': u'S11,59,GN',
                  u'coach_position': 0,
                  u'current_status': u'CNF',
                  u'no': 1},
                 {u'booking_status': u'S11,62,GN',
                  u'coach_position': 0,
                  u'current_status': u'CNF',
                  u'no': 2},
                 {u'booking_status': u'S11,58,GN',
                  u'coach_position': 0,
                  u'current_status': u'CNF',
                  u'no': 3},
                 {u'booking_status': u'S11,61,GN',
                  u'coach_position': 0,
                  u'current_status': u'CNF',
                  u'no': 4}],
 u'pnr': u'4323897189',
 u'reservation_upto': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
 u'response_code': 200,
 u'to_station': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
 u'total_passengers': 4,
 u'train_name': u'SIMHAPURI EXP',
 u'train_num': u'12709',
 u'train_start_date': {u'day': 25, u'month': 9, u'year': 2016}}

 """


def get_train_route_Niraj(train_no):
    print "== in get_train_route_Niraj =%s " %train_no
    url_pnr = "http://api.railwayapi.com/route/train/"

    url_pnr = url_pnr + train_no + '/apikey/' #+ RailwayAPI_APIKEY #+ '/'
    url_pnr = url_pnr + RailwayAPI_APIKEY + '/'
    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)

    response_code = request_data['response_code']
    train_route = request_data['route']
    train_days = request_data['train']['days']
    train_name = request_data['train']['name']
    train_number = request_data['train']['number']

    print "response_code=%s" %response_code
    print "train_route=%s" %train_route
    print "train_days=%s" %train_days
    print "train_name=%s" %train_name
    print "train_number=%s" %train_number

    context = {
               'response_code': response_code,
               'train_route': train_route,
               'train_days': train_days,
               'train_name': train_name,
               'train_number': train_number,
               }

    return context


def get_train_live_status_Niraj(train_no,train_date):
    url_pnr = "http://api.railwayapi.com/live/train/"
    url_pnr = url_pnr + train_no + "/doj/" + train_date + "/apikey/" + RailwayAPI_APIKEY +"/"
    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)

    response_code = request_data['response_code']
    current_station = request_data['current_station']
    position = request_data['position']
    route = request_data['route']
    start_date = request_data['start_date']
    train_number = request_data['train_number']
    error = request_data['error']


    """
    station_CN = {'station_CN':current_station['station_']}
    current_station.update(station_CN)
    print current_station
    for routeloop in route:
        station_CN = {'station_CN':routeloop['station_']}
        routeloop.update(station_CN)
    print route
    """

    context = {
               'response_code': response_code,
               'current_station': current_station,
               'position': position,
               'route': route,
               'start_date': start_date,
               'train_number': train_number,
                'error':error,
               }
    return context



"""
{u'current_station': {u'actarr': u'14:20',
                      u'actarr_date': u'26 Sep 2016',
                      u'actdep': u'14:23',
                      u'day': 1,
                      u'distance': 890,
                      u'has_arrived': True,
                      u'has_departed': True,
                      u'latemin': 8,
                      u'no': 22,
                      u'scharr': u'14:12',
                      u'scharr_date': u'26 Sep 2016',
                      u'schdep': u'14:15',
                      u'station': u'BZU',
                      u'station_': {u'code': u'BZU', u'name': u'BETUL'},
                      u'status': u'8 mins late'},
 u'error': u'',
 u'position': u'Train departed from BETUL(BZU) and late by 8 minutes.',
 u'response_code': 200,
 u'route': [{u'actarr': u'00:00',
             u'actarr_date': u'25 Sep 2016',
             u'actdep': u'23:00',
             u'day': 0,
             u'distance': 0,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 0,
             u'no': 1,
             u'scharr': u'Source',
             u'scharr_date': u'25 Sep 2016',
             u'schdep': u'23:00',
             u'station': u'NZM',
             u'station_': {u'code': u'NZM', u'name': u'HAZRAT NIZAMUDDIN'},
             u'status': u'0 mins late'},
            {u'actarr': u'23:21',
             u'actarr_date': u'25 Sep 2016',
             u'actdep': u'23:23',
             u'day': 0,
             u'distance': 20,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 3,
             u'no': 2,
             u'scharr': u'23:18',
             u'scharr_date': u'25 Sep 2016',
             u'schdep': u'23:20',
             u'station': u'FDB',
             u'station_': {u'code': u'FDB', u'name': u'FARIDABAD'},
             u'status': u'3 mins late'},
            {u'actarr': u'23:33',
             u'actarr_date': u'25 Sep 2016',
             u'actdep': u'23:35',
             u'day': 0,
             u'distance': 28,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 2,
             u'no': 3,
             u'scharr': u'23:31',
             u'scharr_date': u'25 Sep 2016',
             u'schdep': u'23:33',
             u'station': u'BVH',
             u'station_': {u'code': u'BVH', u'name': u'BALLABGARH'},
             u'status': u'2 mins late'},
            {u'actarr': u'00:40',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'00:42',
             u'day': 1,
             u'distance': 92,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 20,
             u'no': 4,
             u'scharr': u'00:20',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'00:22',
             u'station': u'KSV',
             u'station_': {u'code': u'KSV', u'name': u'KOSI KALAN'},
             u'status': u'20 mins late'},
            {u'actarr': u'01:13',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'01:20',
             u'day': 1,
             u'distance': 133,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 18,
             u'no': 5,
             u'scharr': u'00:55',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'01:00',
             u'station': u'MTJ',
             u'station_': {u'code': u'MTJ', u'name': u'MATHURA JN'},
             u'status': u'18 mins late'},
            {u'actarr': u'02:04',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'02:06',
             u'day': 1,
             u'distance': 187,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 9,
             u'no': 6,
             u'scharr': u'01:55',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'02:00',
             u'station': u'AGC',
             u'station_': {u'code': u'AGC', u'name': u'AGRA CANTT'},
             u'status': u'9 mins late'},
            {u'actarr': u'03:36',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'03:38',
             u'day': 1,
             u'distance': 267,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 24,
             u'no': 7,
             u'scharr': u'03:12',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'03:14',
             u'station': u'MRA',
             u'station_': {u'code': u'MRA', u'name': u'MORENA'},
             u'status': u'24 mins late'},
            {u'actarr': u'04:14',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'04:18',
             u'day': 1,
             u'distance': 305,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 31,
             u'no': 8,
             u'scharr': u'03:43',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'03:48',
             u'station': u'GWL',
             u'station_': {u'code': u'GWL', u'name': u'GWALIOR JN.'},
             u'status': u'31 mins late'},
            {u'actarr': u'05:20',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'05:22',
             u'day': 1,
             u'distance': 378,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 35,
             u'no': 9,
             u'scharr': u'04:45',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'04:47',
             u'station': u'DAA',
             u'station_': {u'code': u'DAA', u'name': u'DATIA'},
             u'status': u'35 mins late'},
            {u'actarr': u'05:50',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'06:00',
             u'day': 1,
             u'distance': 402,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 30,
             u'no': 10,
             u'scharr': u'05:20',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'05:30',
             u'station': u'JHS',
             u'station_': {u'code': u'JHS', u'name': u'JHANSI JN'},
             u'status': u'30 mins late'},
            {u'actarr': u'06:26',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'06:28',
             u'day': 1,
             u'distance': 426,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 31,
             u'no': 11,
             u'scharr': u'05:55',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'05:57',
             u'station': u'BAB',
             u'station_': {u'code': u'BAB', u'name': u'BABINA'},
             u'status': u'31 mins late'},
            {u'actarr': u'07:12',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'07:14',
             u'day': 1,
             u'distance': 491,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 30,
             u'no': 12,
             u'scharr': u'06:42',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'06:44',
             u'station': u'LAR',
             u'station_': {u'code': u'LAR', u'name': u'LALITPUR'},
             u'status': u'30 mins late'},
            {u'actarr': u'08:10',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'08:15',
             u'day': 1,
             u'distance': 553,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 15,
             u'no': 13,
             u'scharr': u'07:55',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'08:00',
             u'station': u'BINA',
             u'station_': {u'code': u'BINA', u'name': u'BINA JN'},
             u'status': u'15 mins late'},
            {u'actarr': u'08:37',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'08:39',
             u'day': 1,
             u'distance': 571,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 22,
             u'no': 14,
             u'scharr': u'08:15',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'08:17',
             u'station': u'MABA',
             u'station_': {u'code': u'MABA', u'name': u'MANDI BAMORA'},
             u'status': u'22 mins late'},
            {u'actarr': u'09:00',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'09:02',
             u'day': 1,
             u'distance': 599,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 19,
             u'no': 15,
             u'scharr': u'08:41',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'08:43',
             u'station': u'BAQ',
             u'station_': {u'code': u'BAQ', u'name': u'GANJ BASODA'},
             u'status': u'19 mins late'},
            {u'actarr': u'09:32',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'09:34',
             u'day': 1,
             u'distance': 639,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 23,
             u'no': 16,
             u'scharr': u'09:09',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'09:11',
             u'station': u'BHS',
             u'station_': {u'code': u'BHS', u'name': u'VIDISHA'},
             u'status': u'23 mins late'},
            {u'actarr': u'10:35',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'10:40',
             u'day': 1,
             u'distance': 692,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 25,
             u'no': 17,
             u'scharr': u'10:10',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'10:15',
             u'station': u'BPL',
             u'station_': {u'code': u'BPL', u'name': u'BHOPAL  JN'},
             u'status': u'25 mins late'},
            {u'actarr': u'10:52',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'10:54',
             u'day': 1,
             u'distance': 698,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 22,
             u'no': 18,
             u'scharr': u'10:30',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'10:32',
             u'station': u'HBJ',
             u'station_': {u'code': u'HBJ', u'name': u'HABIBGANJ'},
             u'status': u'22 mins late'},
            {u'actarr': u'11:53',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'11:55',
             u'day': 1,
             u'distance': 766,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 23,
             u'no': 19,
             u'scharr': u'11:30',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'11:32',
             u'station': u'HBD',
             u'station_': {u'code': u'HBD', u'name': u'HOSHANGABAD'},
             u'status': u'23 mins late'},
            {u'actarr': u'12:25',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'12:30',
             u'day': 1,
             u'distance': 783,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 10,
             u'no': 20,
             u'scharr': u'12:15',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'12:20',
             u'station': u'ET',
             u'station_': {u'code': u'ET', u'name': u'ITARSI JN'},
             u'status': u'10 mins late'},
            {u'actarr': u'13:39',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'13:41',
             u'day': 1,
             u'distance': 854,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 16,
             u'no': 21,
             u'scharr': u'13:23',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'13:25',
             u'station': u'GDYA',
             u'station_': {u'code': u'GDYA', u'name': u'GHORADONGRI'},
             u'status': u'16 mins late'},
            {u'actarr': u'14:20',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'14:23',
             u'day': 1,
             u'distance': 890,
             u'has_arrived': True,
             u'has_departed': True,
             u'latemin': 8,
             u'no': 22,
             u'scharr': u'14:12',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'14:15',
             u'station': u'BZU',
             u'station_': {u'code': u'BZU', u'name': u'BETUL'},
             u'status': u'8 mins late'},
            {u'actarr': u'14:42',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'14:44',
             u'day': 1,
             u'distance': 913,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 1,
             u'no': 23,
             u'scharr': u'14:41',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'14:43',
             u'station': u'AMLA',
             u'station_': {u'code': u'AMLA', u'name': u'AMLA JN'},
             u'status': u'1 mins late'},
            {u'actarr': u'14:58',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'15:00',
             u'day': 1,
             u'distance': 936,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 1,
             u'no': 24,
             u'scharr': u'14:57',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'14:59',
             u'station': u'MTY',
             u'station_': {u'code': u'MTY', u'name': u'MULTAI'},
             u'status': u'1 mins late'},
            {u'actarr': u'15:45',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'15:47',
             u'day': 1,
             u'distance': 977,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 25,
             u'scharr': u'15:45',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'15:47',
             u'station': u'PAR',
             u'station_': {u'code': u'PAR', u'name': u'PANDHURNA'},
             u'status': u'0 mins late'},
            {u'actarr': u'16:00',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'16:02',
             u'day': 1,
             u'distance': 995,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 26,
             u'scharr': u'16:00',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'16:02',
             u'station': u'NRKR',
             u'station_': {u'code': u'NRKR', u'name': u'NARKHER'},
             u'status': u'0 mins late'},
            {u'actarr': u'16:22',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'16:24',
             u'day': 1,
             u'distance': 1020,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 27,
             u'scharr': u'16:22',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'16:24',
             u'station': u'KATL',
             u'station_': {u'code': u'KATL', u'name': u'KATOL'},
             u'status': u'0 mins late'},
            {u'actarr': u'17:35',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'17:45',
             u'day': 1,
             u'distance': 1081,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 28,
             u'scharr': u'17:35',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'17:45',
             u'station': u'NGP',
             u'station_': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'status': u'0 mins late'},
            {u'actarr': u'18:19',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'18:21',
             u'day': 1,
             u'distance': 1126,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 29,
             u'scharr': u'18:19',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'18:21',
             u'station': u'SNI',
             u'station_': {u'code': u'SNI', u'name': u'SINDI'},
             u'status': u'0 mins late'},
            {u'actarr': u'18:51',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'18:53',
             u'day': 1,
             u'distance': 1157,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 30,
             u'scharr': u'18:51',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'18:53',
             u'station': u'SEGM',
             u'station_': {u'code': u'SEGM', u'name': u'SEVAGRAM'},
             u'status': u'0 mins late'},
            {u'actarr': u'19:21',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'19:23',
             u'day': 1,
             u'distance': 1194,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 31,
             u'scharr': u'19:21',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'19:23',
             u'station': u'HGT',
             u'station_': {u'code': u'HGT', u'name': u'HINGANGHAT'},
             u'status': u'0 mins late'},
            {u'actarr': u'19:53',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'19:55',
             u'day': 1,
             u'distance': 1232,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 32,
             u'scharr': u'19:53',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'19:55',
             u'station': u'WRR',
             u'station_': {u'code': u'WRR', u'name': u'WARORA'},
             u'status': u'0 mins late'},
            {u'actarr': u'20:14',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'20:16',
             u'day': 1,
             u'distance': 1253,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 33,
             u'scharr': u'20:14',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'20:16',
             u'station': u'BUX',
             u'station_': {u'code': u'BUX', u'name': u'BHANDAK'},
             u'status': u'0 mins late'},
            {u'actarr': u'20:45',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'20:48',
             u'day': 1,
             u'distance': 1278,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 34,
             u'scharr': u'20:45',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'20:48',
             u'station': u'CD',
             u'station_': {u'code': u'CD', u'name': u'CHANDRAPUR'},
             u'status': u'0 mins late'},
            {u'actarr': u'21:45',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'22:00',
             u'day': 1,
             u'distance': 1292,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 35,
             u'scharr': u'21:45',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'22:00',
             u'station': u'BPQ',
             u'station_': {u'code': u'BPQ', u'name': u'BALHARSHAH'},
             u'status': u'0 mins late'},
            {u'actarr': u'22:48',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'22:50',
             u'day': 1,
             u'distance': 1361,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 36,
             u'scharr': u'22:48',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'22:50',
             u'station': u'SKZR',
             u'station_': {u'code': u'SKZR', u'name': u'SIRPUR KAGAZNGR'},
             u'status': u'0 mins late'},
            {u'actarr': u'23:13',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'23:15',
             u'day': 1,
             u'distance': 1400,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 37,
             u'scharr': u'23:13',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'23:15',
             u'station': u'BPA',
             u'station_': {u'code': u'BPA', u'name': u'BELAMPALLI'},
             u'status': u'0 mins late'},
            {u'actarr': u'23:30',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'23:32',
             u'day': 1,
             u'distance': 1420,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 38,
             u'scharr': u'23:30',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'23:32',
             u'station': u'MCI',
             u'station_': {u'code': u'MCI', u'name': u'MANCHERAL'},
             u'status': u'0 mins late'},
            {u'actarr': u'23:41',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'23:43',
             u'day': 1,
             u'distance': 1433,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 39,
             u'scharr': u'23:41',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'23:43',
             u'station': u'RDM',
             u'station_': {u'code': u'RDM', u'name': u'RAMGUNDAM'},
             u'status': u'0 mins late'},
            {u'actarr': u'23:53',
             u'actarr_date': u'26 Sep 2016',
             u'actdep': u'23:55',
             u'day': 1,
             u'distance': 1451,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 40,
             u'scharr': u'23:53',
             u'scharr_date': u'26 Sep 2016',
             u'schdep': u'23:55',
             u'station': u'PDPL',
             u'station_': {u'code': u'PDPL', u'name': u'PEDDAPALLI'},
             u'status': u'0 mins late'},
            {u'actarr': u'00:23',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'00:25',
             u'day': 2,
             u'distance': 1490,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 41,
             u'scharr': u'00:23',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'00:25',
             u'station': u'JMKT',
             u'station_': {u'code': u'JMKT', u'name': u'JAMIKUNTA'},
             u'status': u'0 mins late'},
            {u'actarr': u'01:20',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'01:40',
             u'day': 2,
             u'distance': 1535,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 42,
             u'scharr': u'01:20',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'01:40',
             u'station': u'KZJ',
             u'station_': {u'code': u'KZJ', u'name': u'KAZIPET JN'},
             u'status': u'0 mins late'},
            {u'actarr': u'02:08',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'02:10',
             u'day': 2,
             u'distance': 1584,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 43,
             u'scharr': u'02:08',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'02:10',
             u'station': u'ZN',
             u'station_': {u'code': u'ZN', u'name': u'JANGAON'},
             u'status': u'0 mins late'},
            {u'actarr': u'02:48',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'02:50',
             u'day': 2,
             u'distance': 1621,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 44,
             u'scharr': u'02:48',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'02:50',
             u'station': u'BG',
             u'station_': {u'code': u'BG', u'name': u'BHONGIR'},
             u'status': u'0 mins late'},
            {u'actarr': u'04:05',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'04:10',
             u'day': 2,
             u'distance': 1675,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 45,
             u'scharr': u'04:05',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'04:10',
             u'station': u'SC',
             u'station_': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'status': u'0 mins late'},
            {u'actarr': u'05:00',
             u'actarr_date': u'27 Sep 2016',
             u'actdep': u'00:00',
             u'day': 2,
             u'distance': 1684,
             u'has_arrived': False,
             u'has_departed': False,
             u'latemin': 0,
             u'no': 46,
             u'scharr': u'05:00',
             u'scharr_date': u'27 Sep 2016',
             u'schdep': u'Destination',
             u'station': u'HYB',
             u'station_': {u'code': u'HYB', u'name': u'HYDERABAD DECAN'},
             u'status': u'0 mins late'}],
 u'start_date': u'25 Sep 2016',
 u'train_number': u'12722'}
>>>
"""



def get_seat_availability_Niraj(trainno,Source_station_code,
                                Destination_station_code,train_date,
                                train_class,train_quota):
    print "trainno=%s" %trainno
    print "Source_station_code=%s" %Source_station_code
    print "Destination_station_code=%s" %Destination_station_code
    print "train_date=%s" %train_date
    print "train_class=%s" %train_class
    print "train_quota=%s" %train_quota

    #http://api.railwayapi.com/check_seat/train/<train number>/source/<source code>/dest/<dest code>/date/<doj in DD-MM-YYYY>/class/<class code>/quota/<quota code>/apikey/<apikey>/


    url_pnr = "http://api.railwayapi.com/check_seat/train/"
    url_pnr = url_pnr + trainno + "/source/" + Source_station_code + "/dest/" + Destination_station_code + "/date/" + train_date + "/class/" + train_class + "/quota/" + train_quota + "/apikey/" + RailwayAPI_APIKEY + "/"

    print "get_seat_availability_Niraj url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'error': Error_str,
                   }
         return context

    print "response=%s" %response
    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)

    from_station = {}
    to_station = {}
    train_class = {}
    train_name = {}
    train_number = {}
    availability = {}
    last_updated = {}
    quota = {}
    error = {}

    response_code = request_data['response_code']

    if response_code == 200:
        from_station = request_data['from']
        to_station = request_data['to']
        train_class = request_data['class']
        train_name = request_data['train_name']
        train_number = request_data['train_number']
        availability = request_data['availability']
        last_updated = request_data['last_updated']
        quota = request_data['quota']
        error = request_data['error']
    else:
        error = request_data['error']

    context = {
               'response_code': response_code,
               'from_station': from_station,
               'to_station': to_station,
               'train_class': train_class,
               'train_name': train_name,
               'train_number': train_number,
               'availability': availability,
               'last_updated': last_updated,
               'quota' : quota,
               'error' : error,
               }
    return context



"""
url_pnr=http://api.railwayapi.com/check_seat/train/12771/source/sc/dest/ngp/date/30-09-2016/class/SL/quota/GN/apikey/joymo1655/
{u'availability': [{u'date': u'30-9-2016', u'status': u'GNWL111/WL63'},
                   {u'date': u'3-10-2016', u'status': u'RAC55/RAC 47'},
                   {u'date': u'5-10-2016', u'status': u'AVAILABLE 61'},
                   {u'date': u'7-10-2016', u'status': u'GNWL196/WL144'},
                   {u'date': u'10-10-2016', u'status': u'RAC6/RAC 6'},
                   {u'date': u'12-10-2016', u'status': u'AVAILABLE 89'}],
 u'class': {u'class_code': u'SL', u'class_name': u'SLEEPER CLASS'},
 u'error': u'',
 u'failure_rate': 52.43128964059197,
 u'from': {u'code': u'SC',
           u'lat': 0.0,
           u'lng': 0.0,
           u'name': u'SECUNDERABAD JN'},
 u'last_updated': {u'date': u'2016-09-28', u'time': u'18:34'},
 u'quota': {u'quota_code': u'GN', u'quota_name': u'GENERAL QUOTA'},
 u'response_code': 200,
 u'to': {u'code': u'NGP',
         u'lat': 21.152187,
         u'lng': 79.0887588,
         u'name': u'NAGPUR'},
 u'train_name': u'SC NGP SUP EXP',
 u'train_number': u'12771'}
"""



def get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date):
    url_pnr = "http://api.railwayapi.com/between/source/"
    url_pnr = url_pnr + Source_station_code + "/dest/" + Destination_station_code + "/date/" + train_date + "/apikey/" + RailwayAPI_APIKEY + "/"

    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'error': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)

    train = {}
    total = {}
    error = {}

    response_code = request_data['response_code']
    if response_code == 200:
        train = request_data['train']
        total = request_data['total']


    #print "==>%s" %train[0]['classes'][0]['class-code']

    for trainvar in train:
        for classesvar in trainvar['classes']:
            append_class = {'class_code':classesvar['class-code']}
            classesvar.update(append_class)
            #print "1==>%s" %classesvar

        for daysvar in trainvar['days']:
            append_day = {'day_code':daysvar['day-code']}
            daysvar.update(append_day)
            #print "1==>%s" %daysvar
        #print "endl"

       #if trainvar['classes']['available']=='Y':
       #     print "==>%s" %trainvar['classes']['class-code']

    context = {
               'response_code': response_code,
               'train': train,
               'total': total,
                'error': error,
               }

    return context


"""
url_pnr=http://api.railwayapi.com/between/source/sc/dest/ngp/date/30-09/apikey/joymo1655/
{u'error': u'',
 u'response_code': 200,
 u'total': 9,
 u'train': [{u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'Y', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'N'},
                       {u'day-code': u'TUE', u'runs': u'N'},
                       {u'day-code': u'WED', u'runs': u'N'},
                       {u'day-code': u'THU', u'runs': u'N'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'Y'}],
             u'dest_arrival_time': u'11:05',
             u'from': {u'code': u'KCG', u'name': u'KACHEGUDA'},
             u'name': u'MYS-JP EXPRESS',
             u'no': 1,
             u'number': u'12975',
             u'src_departure_time': u'02:10',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'08:55'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'Y', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'Y'},
                       {u'day-code': u'WED', u'runs': u'Y'},
                       {u'day-code': u'THU', u'runs': u'Y'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'Y'},
                       {u'day-code': u'SUN', u'runs': u'Y'}],
             u'dest_arrival_time': u'15:40',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'TELANGANA EXPRESS',
             u'no': 2,
             u'number': u'12723',
             u'src_departure_time': u'06:50',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'08:50'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'N'},
                       {u'day-code': u'TUE', u'runs': u'N'},
                       {u'day-code': u'WED', u'runs': u'N'},
                       {u'day-code': u'THU', u'runs': u'N'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'N'}],
             u'dest_arrival_time': u'17:00',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'SC-GKP EXP',
             u'no': 3,
             u'number': u'12590',
             u'src_departure_time': u'07:20',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'09:40'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'N', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'Y', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'Y'},
                       {u'day-code': u'WED', u'runs': u'N'},
                       {u'day-code': u'THU', u'runs': u'Y'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'N'}],
             u'dest_arrival_time': u'15:20',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'BANGALORE RAJDHANI EXPRES',
             u'no': 4,
             u'number': u'22691',
             u'src_departure_time': u'07:50',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'07:30'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'Y'},
                       {u'day-code': u'WED', u'runs': u'Y'},
                       {u'day-code': u'THU', u'runs': u'Y'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'Y'},
                       {u'day-code': u'SUN', u'runs': u'Y'}],
             u'dest_arrival_time': u'19:15',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'SC-DNR EXP',
             u'no': 5,
             u'number': u'12791',
             u'src_departure_time': u'10:00',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'09:15'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'N'},
                       {u'day-code': u'TUE', u'runs': u'N'},
                       {u'day-code': u'WED', u'runs': u'N'},
                       {u'day-code': u'THU', u'runs': u'N'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'N'}],
             u'dest_arrival_time': u'00:45',
             u'from': {u'code': u'KCG', u'name': u'KACHEGUDA'},
             u'name': u'YPR-GKP-EXP',
             u'no': 6,
             u'number': u'15024',
             u'src_departure_time': u'10:40',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'14:05'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'N'},
                       {u'day-code': u'WED', u'runs': u'Y'},
                       {u'day-code': u'THU', u'runs': u'N'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'N'}],
             u'dest_arrival_time': u'02:00',
             u'from': {u'code': u'KCG', u'name': u'KACHEGUDA'},
             u'name': u'TPTY-NZM AP SAMPRK KRANTI',
             u'no': 7,
             u'number': u'12707',
             u'src_departure_time': u'17:15',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'08:45'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'N'},
                       {u'day-code': u'WED', u'runs': u'Y'},
                       {u'day-code': u'THU', u'runs': u'N'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'N'},
                       {u'day-code': u'SUN', u'runs': u'N'}],
             u'dest_arrival_time': u'08:15',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'SC-NGP  EXP',
             u'no': 8,
             u'number': u'12771',
             u'src_departure_time': u'22:00',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'10:15'},
            {u'classes': [{u'available': u'Y', u'class-code': u'3A'},
                          {u'available': u'N', u'class-code': u'3E'},
                          {u'available': u'Y', u'class-code': u'SL'},
                          {u'available': u'N', u'class-code': u'FC'},
                          {u'available': u'N', u'class-code': u'1A'},
                          {u'available': u'Y', u'class-code': u'2A'},
                          {u'available': u'N', u'class-code': u'CC'},
                          {u'available': u'N', u'class-code': u'2S'}],
             u'days': [{u'day-code': u'MON', u'runs': u'Y'},
                       {u'day-code': u'TUE', u'runs': u'Y'},
                       {u'day-code': u'WED', u'runs': u'Y'},
                       {u'day-code': u'THU', u'runs': u'Y'},
                       {u'day-code': u'FRI', u'runs': u'Y'},
                       {u'day-code': u'SAT', u'runs': u'Y'},
                       {u'day-code': u'SUN', u'runs': u'Y'}],
             u'dest_arrival_time': u'09:05',
             u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
             u'name': u'HYB-NZM DAKSHIN EXP',
             u'no': 9,
             u'number': u'12721',
             u'src_departure_time': u'23:00',
             u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
             u'travel_time': u'10:05'}]}


"""


def get_train_Name_Number_Niraj(train_Name_Number):
    url_pnr = "http://api.railwayapi.com/name_number/train/"
    url_pnr = url_pnr + train_Name_Number + "/apikey/" + RailwayAPI_APIKEY + "/"

    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)


    response_code = request_data['response_code']
    train = request_data['train']
    #total = request_data['total']
    #error = request_data['error']

    #print "==>%s" %train[0]['classes'][0]['class-code']

    for trainvar in train['days']:
        append_class = {'day_code':trainvar['day-code']}
        trainvar.update(append_class)
        #print "1==>%s" %trainvar
        #print "endl"

    context = {
               'response_code': response_code,
               'train': train,
               }

    return context
"""
url_pnr=http://api.railwayapi.com/name_number/train/12771/apikey/joymo1655/
{u'response_code': 200,
 u'train': {u'days': [{u'day-code': u'SUN', u'runs': u'N'},
                      {u'day-code': u'MON', u'runs': u'Y'},
                      {u'day-code': u'TUE', u'runs': u'N'},
                      {u'day-code': u'WED', u'runs': u'Y'},
                      {u'day-code': u'THU', u'runs': u'N'},
                      {u'day-code': u'FRI', u'runs': u'Y'},
                      {u'day-code': u'SAT', u'runs': u'N'}],
            u'name': u'SC NGP SUP EXP',
            u'number': u'12771'}}
"""

def get_Train_Fair_Enquiry_Niraj(Source_station_code,Destination_station_code,
                                                   trainno, Age_of_the_passenger,train_quota,
                                                   train_date):


    url_pnr = "http://api.railwayapi.com/fare/train/"
    url_pnr = url_pnr + trainno + "/source/"+ Source_station_code + "/dest/" + Destination_station_code + "/age/" + Age_of_the_passenger + "/quota/" + train_quota + "/doj/" + train_date  + "/apikey/" + RailwayAPI_APIKEY + "/"

    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)


    response_code = request_data['response_code']
    train = request_data['train']
    fare = request_data['fare']
    from_train = request_data['from']
    quota = request_data['quota']
    to_train = request_data['to']

    context = {
               'response_code': response_code,
               'train': train,
               'fare':fare,
               'from_train':from_train,
               'quota':quota,
               'to_train':to_train,
               }
    return context


"""
url_pnr=http://api.railwayapi.com/fare/train/12771/source/sc/dest/ngp/age/27/quota/GN/doj/07-10-2016/apikey/joymo1655/
{u'failure_rate': 14.885496183206106,
 u'fare': [{u'code': u'2A', u'fare': u'1305', u'name': u'SECOND AC'},
           {u'code': u'3A', u'fare': u'925', u'name': u'THIRD AC'},
           {u'code': u'SL', u'fare': u'355', u'name': u'SLEEPER CLASS'}],
 u'from': {u'code': u'SC', u'name': u'SECUNDERABAD JN'},
 u'quota': {u'code': u'GN', u'name': u'GENERAL QUOTA'},
 u'response_code': 200,
 u'to': {u'code': u'NGP', u'name': u'NAGPUR'},
 u'train': {u'name': u'SC NGP SUP EXP', u'number': u'12771'}}
"""


def get_train_Arrivals_At_Station_Niraj(stationCode):
    url_pnr = "http://api.railwayapi.com/arrivals/station/"
    url_pnr = url_pnr + stationCode + "/hours/" + "4" + "/apikey/" + RailwayAPI_APIKEY + "/"
    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'Error_str': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)


    response_code = request_data['response_code']
    train = request_data['train']
    total = request_data['total']
    #error = request_data['error']

    context = {
               'response_code': response_code,
               'train': train,
               'total':total,
               }

    return context


"""
url_pnr=http://api.railwayapi.com/arrivals/station/SC/hours/2/apikey/joymo1655/
{u'response_code': 200,
 u'station': u'SC',
 u'total': 30,
 u'train': [{u'actarr': u'17:39',
             u'actdep': u'17:40',
             u'delayarr': u'00:04',
             u'delaydep': u'RT',
             u'name': u'HYB-VSKP GODAVARI EXP',
             u'number': u'12728',
             u'scharr': u'17:35',
             u'schdep': u'17:40'},

            {u'actarr': u'17:40',
             u'actdep': u'17:42',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'FM-LPI',
             u'number': u'47163',
             u'scharr': u'17:40',
             u'schdep': u'17:42'},
            {u'actarr': u'17:40',
             u'actdep': u'17:50',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'BBS-PUNE S/F WEEKLY',
             u'number': u'22882',
             u'scharr': u'17:40',
             u'schdep': u'17:50'},
            {u'actarr': u'17:47',
             u'actdep': u'17:52',
             u'delayarr': u'04:32',
             u'delaydep': u'04:32',
             u'name': u'VKB-KCG PASSENGER',
             u'number': u'57606',
             u'scharr': u'13:15',
             u'schdep': u'13:20'},
            {u'actarr': u'17:53',
             u'actdep': u'17:55',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'LPI-FM',
             u'number': u'47187',
             u'scharr': u'17:53',
             u'schdep': u'17:55'},
            {u'actarr': u'SRC',
             u'actdep': u'18:00',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-TDU',
             u'number': u'67250',
             u'scharr': u'SRC',
             u'schdep': u'18:00'},
            {u'actarr': u'SRC',
             u'actdep': u'18:05',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-TPTY NARAYANADRI EXP',
             u'number': u'12734',
             u'scharr': u'SRC',
             u'schdep': u'18:05'},
            {u'actarr': u'SRC',
             u'actdep': u'18:10',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-MMR AJANTHA EXP',
             u'number': u'17064',
             u'scharr': u'SRC',
             u'schdep': u'18:10'},
            {u'actarr': u'18:10',
             u'actdep': u'18:11',
             u'delayarr': u'00:40',
             u'delaydep': u'00:40',
             u'name': u'PUSHPULL',
             u'number': u'67267',
             u'scharr': u'17:30',
             u'schdep': u'17:31'},
            {u'actarr': u'18:08',
             u'actdep': u'18:17',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'FM-LPI',
             u'number': u'47164',
             u'scharr': u'18:08',
             u'schdep': u'18:17'},
            {u'actarr': u'18:20',
             u'actdep': u'18:22',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-FM',
             u'number': u'47210',
             u'scharr': u'18:20',
             u'schdep': u'18:22'},
            {u'actarr': u'SRC',
             u'actdep': u'18:22',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-MOB DEMU',
             u'number': u'77617',
             u'scharr': u'SRC',
             u'schdep': u'18:22'},
            {u'actarr': u'18:20',
             u'actdep': u'18:25',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-TPTY HSP',
             u'number': u'02764',
             u'scharr': u'18:20',
             u'schdep': u'18:25'},
            {u'actarr': u'SRC',
             u'actdep': u'18:30',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-BIDR-INTER CITY EXP',
             u'number': u'17010',
             u'scharr': u'SRC',
             u'schdep': u'18:30'},
            {u'actarr': u'18:30',
             u'actdep': u'18:35',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'FM-LPI',
             u'number': u'47218',
             u'scharr': u'18:30',
             u'schdep': u'18:35'},
            {u'actarr': u'SRC',
             u'actdep': u'18:40',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-MUGR FAST PASS',
             u'number': u'57625',
             u'scharr': u'SRC',
             u'schdep': u'18:40'},
            {u'actarr': u'18:35',
             u'actdep': u'18:50',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'BANGALORE RAJDHANI EXPRES',
             u'number': u'22692',
             u'scharr': u'18:35',
             u'schdep': u'18:50'},
            {u'actarr': u'18:50',
             u'actdep': u'18:55',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'HYB-MAS CHARMINAR EXP',
             u'number': u'12760',
             u'scharr': u'18:50',
             u'schdep': u'18:55'},
            {u'actarr': u'18:55',
             u'actdep': u'18:57',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'LPI-FM',
             u'number': u'47188',
             u'scharr': u'18:55',
             u'schdep': u'18:57'},
            {u'actarr': u'19:00',
             u'actdep': u'19:05',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'TELANGANA EXPRESS',
             u'number': u'12724',
             u'scharr': u'19:00',
             u'schdep': u'19:05'},
            {u'actarr': u'19:10',
             u'actdep': u'19:11',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'PUSHPULL',
             u'number': u'67266',
             u'scharr': u'19:10',
             u'schdep': u'19:11'},
            {u'actarr': u'19:14',
             u'actdep': u'19:19',
             u'delayarr': u'00:09',
             u'delaydep': u'00:09',
             u'name': u'FM PASS',
             u'number': u'57659',
             u'scharr': u'19:05',
             u'schdep': u'19:10'},
            {u'actarr': u'19:20',
             u'actdep': u'19:24',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'FM-LPI',
             u'number': u'47166',
             u'scharr': u'19:20',
             u'schdep': u'19:24'},
            {u'actarr': u'19:25',
             u'actdep': u'19:27',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'LPI-FM',
             u'number': u'47190',
             u'scharr': u'19:25',
             u'schdep': u'19:27'},
            {u'actarr': u'19:28',
             u'actdep': u'19:33',
             u'delayarr': u'00:28',
             u'delaydep': u'00:28',
             u'name': u'TELANGANA EXPRESS',
             u'number': u'12724',
             u'scharr': u'19:00',
             u'schdep': u'19:05'},
            {u'actarr': u'19:40',
             u'actdep': u'19:42',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'SC-FM',
             u'number': u'47207',
             u'scharr': u'19:40',
             u'schdep': u'19:42'},
            {u'actarr': u'18:17',
             u'actdep': u'DSTN',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'UR-SC DEMU',
             u'number': u'77645',
             u'scharr': u'18:17',
             u'schdep': u'DSTN'},
            {u'actarr': u'18:17',
             u'actdep': u'DSTN',
             u'delayarr': u'RT',
             u'delaydep': u'RT',
             u'name': u'MOB-SC DEMU',
             u'number': u'77614',
             u'scharr': u'18:17',
             u'schdep': u'DSTN'},
            {u'actarr': u'18:15',
             u'actdep': u'DSTN',
             u'delayarr': u'00:30',
             u'delaydep': u'RT',
             u'name': u'SKZR-SC-INTERCITY',
             u'number': u'17012',
             u'scharr': u'17:45',
             u'schdep': u'DSTN'},
            {u'actarr': u'19:08',
             u'actdep': u'DSTN',
             u'delayarr': u'00:23',
             u'delaydep': u'RT',
             u'name': u'VSKP-SC JANMABHOOMI',
             u'number': u'12805',
             u'scharr': u'18:45',
             u'schdep': u'DSTN'}]}
"""


def get_cancelled_Trains_Niraj(train_date):
    url_pnr = "http://api.railwayapi.com/cancelled/date/"
    url_pnr = url_pnr + train_date + "/apikey/" + RailwayAPI_APIKEY + "/"

    #url_pnr = "http://api.railwayapi.com/cancelled/date/01-10-2016/apikey/joymo1655/"
    print "url_pnr=%s " %url_pnr
    request_data = {}
    context = {}
    try:
        response = urllib2.urlopen(url_pnr)
    except urllib2.HTTPError as e:
         content = e.read()
         Error_str = content[content.find('<title>')+7:content.find('</title>')]
         Error_str = Error_str + '\n' + content[content.find('<p>')+3:content.find('</p>')]
         print "error_msg=%s" %Error_str
         context = {
                   'response_code': 500,
                   'error': Error_str,
                   }
         return context

    headers = response.info()
    data_file = response.read()
    #print "data_file=%s " %data_file
    request_data = json.loads(data_file)
    pprint(request_data)

    last_updated = {}
    trains = {}
    error = {}

    response_code = request_data['response_code']

    if response_code == 200:
        last_updated = request_data['last_updated']
        trains = request_data['trains']
    else:
        error = 'Error in Received Data'#request_data['error']
        last_updated = request_data['last_updated']
        trains = request_data['trains']

    context = {
               'response_code': response_code,
               'last_updated': last_updated,
               'trains':trains,
               'error':error,
               }

    return context


def get_pnr_status_for_alert_Niraj(pnr_notify, delete_on_fail=True):
    pnr_no = pnr_notify.pnr_no
    p = pnrapi.PnrApi_Niraj(pnr_no,RailwayAPI_APIKEY)

    if not p.request():
        if delete_on_fail:
            pnr_notify.delete()

        """
        send_email(
            message=u'PNR: {} \n\n Error: {}'.format(pnr_no, p.error),
            subject='Py-PNR-Status Error!',
            to_addr='niraj.bilaimare@gmail.com'
        )
        """
        return {'error': p.error}
    resp = p.get_json()

    print "In get_pnr_status resp=%s" %resp


    def _map_passenger(passenger):
        return {
           'seat_number': passenger['current_status'],
           'status': passenger['booking_status']
        }
    passengers = [_map_passenger(key) for key in resp['passengers']]

    ticket_is_cancelled = ticket_is_confirmed = chart_prepared_for_ticket = None
    will_get_notifications = True

    if check_if_ticket_cancelled(passengers):
        ticket_is_cancelled = True
        will_get_notifications = False
    if check_if_passengers_cnf(passengers):
        ticket_is_confirmed = True
        will_get_notifications = False
    if resp['chart_prepared'] == 'Y':
        chart_prepared_for_ticket = True
        will_get_notifications = False

    json_dict =  {'pnr_no': pnr_no,
                  'passengers': passengers,
                  'ticket_is_cancelled': ticket_is_cancelled,
                  'ticket_is_confirmed': ticket_is_confirmed,
                  'chart_prepared_for_ticket': chart_prepared_for_ticket,
                  'will_get_notifications': will_get_notifications,
                  'pnr_notify': pnr_notify }

    pnr_status, cr = PNRStatus.objects.get_or_create(pnr_no=pnr_no)
    pnr_status.status = resp
    pnr_status.save()

    return json_dict
