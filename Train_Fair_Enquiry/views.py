from django.shortcuts import render
from userpanal.pnr_utils import get_Train_Fair_Enquiry_Niraj,get_Train_Between_Stations_Niraj
from django.http import HttpResponse
import json

def trainFairEnquiry(request):
    template_name = 'Train_Fair_Enquiry/trainFairEnquiry.html'
    context = {}
    context['info_page'] = "trainFairEnquiry"
    return render(request,template_name, context)


def train_fair(request):
    if request.method == "POST":
        #trainno = request.POST.get('trainno')
        Source_station_code = request.POST.get('source')
        Destination_station_code = request.POST.get('dest')
        Passenger_Age = request.POST.get('Passenger_Age')
        train_quota = request.POST.get('train_quota')
        train_date = request.POST.get('date')

        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]
        Destination_station_code = Destination_station_code[Destination_station_code.find('-')+2:]
        train_date = train_date[:-5]

        print "Passenger_Age=%s" %Passenger_Age
        #print "trainno=%s" %trainno
        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        context = get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date)

        print "---- Return Data --------"
        return HttpResponse(json.dumps(context), content_type = "application/json")

        #context = get_Train_Fair_Enquiry_Niraj(Source_station_code,Destination_station_code,
                                                   #trainno, Passenger_Age,train_quota,
                                                   #train_date)
        #return render(request,'Train_Fair_Enquiry/trainFairEnquiryDetail.html', context)

def train_fair_detail(request):
    if request.method == "POST":
        print "train_fair_detail(request):"

        Source_station_code = request.POST.get('from_name')
        Destination_station_code = request.POST.get('to_name')
        train_date = request.POST.get('date')
        train_quota = request.POST.get('train_quota')
        trainno = request.POST.get('train_number')
        Passenger_Age = request.POST.get('Passenger_Age')
        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]
        Destination_station_code = Destination_station_code[Destination_station_code.find('-')+2:]


        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date
        print "train_quota=%s" %train_quota

        print "trainno=%s" %trainno

        context = get_Train_Fair_Enquiry_Niraj(Source_station_code,Destination_station_code,
                                                   trainno, Passenger_Age,train_quota,
                                                   train_date)

        return HttpResponse(json.dumps(context), content_type = "application/json")


    return HttpResponse('')
