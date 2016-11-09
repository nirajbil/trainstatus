from django.shortcuts import render
from django.http import HttpResponse
from userpanal.pnr_utils import get_seat_availability_Niraj,get_Train_Between_Stations_Niraj
import json

def seatAvailability(request):
    template_name = 'Seat_Availability/seatAvailability.html'
    context = {}
    context['info_page'] = "seatAvailability"
    """
    if request.method == "GET":
        #trainno = request.POST.get('trainno')
        Source_station_code = request.POST.get('Source_station_code')
        Destination_station_code = request.POST.get('Destination_station_code')
        train_date = request.POST.get('date')
        #train_class = request.POST.get('train_class')
        train_quota = request.POST.get('train_quota')

        #print "trainno=%s" %trainno
        print "GET Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        #print "train_class=%s" %train_class
        print "train_quota=%s" %train_quota


    if request.method == "POST":
        #trainno = request.POST.get('trainno')
        Source_station_code = request.POST.get('Source_station_code')
        Destination_station_code = request.POST.get('Destination_station_code')
        train_date = request.POST.get('date')
        #train_class = request.POST.get('train_class')
        train_quota = request.POST.get('train_quota')

        #print "trainno=%s" %trainno
        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        #print "train_class=%s" %train_class
        print "train_quota=%s" %train_quota


        context = get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date)
        #context = get_seat_availability_Niraj(trainno,Source_station_code, \
                                              #Destination_station_code,train_date,
                                              #train_class,train_quota)
        return render(request,'Seat_Availability/seatAvailabilityDetail.html', context)
    """
    return render(request,template_name, context)


def find_train(request):
    if request.method == "POST":
        data = {}
        print "find_train(request):"
        Source_station_code = request.POST.get('source')
        Destination_station_code = request.POST.get('dest')
        train_date = request.POST.get('date')
        train_quota = request.POST.get('train_quota')
        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]
        Destination_station_code = Destination_station_code[Destination_station_code.find('-')+2:]
        train_date = train_date[:-5]

        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        print "train_quota=%s" %train_quota

        context = get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date)

        print "---- Return Data --------"
        return HttpResponse(json.dumps(context), content_type = "application/json")

def find_seat(request):
    if request.method == "POST":
        print "find_seat(request):"
        train_class = request.POST.get('train_class')
        Source_station_code = request.POST.get('from_name')
        Destination_station_code = request.POST.get('to_name')
        train_date = request.POST.get('date')
        train_quota = request.POST.get('train_quota')
        trainno = request.POST.get('number')
        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]
        Destination_station_code = Destination_station_code[Destination_station_code.find('-')+2:]


        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        print "train_quota=%s" %train_quota
        print "train_class=%s" %train_class
        print "trainno=%s" %trainno

        context = get_seat_availability_Niraj(trainno,Source_station_code,
                                              Destination_station_code,train_date,
                                              train_class,train_quota)

        return HttpResponse(json.dumps(context), content_type = "application/json")



























