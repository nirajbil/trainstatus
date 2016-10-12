from django.shortcuts import render
from userpanal.pnr_utils import get_train_Arrivals_At_Station_Niraj
from django.http import HttpResponse
import json

def trainArrivalsAtStation(request):
    template_name = 'Train_Arrivals_At_Station/trainArrivalsAtStation.html'
    context = {}
    return render(request,template_name, context)


def train_Arrival(request):
    if request.method == "POST":
        Source_station_code = request.POST.get('source')
        print "Source_station_code=%s" %Source_station_code
        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]

        print "Source_station_code=%s" %Source_station_code
        context = get_train_Arrivals_At_Station_Niraj(Source_station_code)

        print "---- Return Data --------"
        return HttpResponse(json.dumps(context), content_type = "application/json")
