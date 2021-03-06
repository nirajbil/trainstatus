from django.shortcuts import render
from userpanal.pnr_utils import get_Train_Between_Stations_Niraj
from django.http import HttpResponse
import json

def trainBetweenStations(request):
    template_name = 'Train_Between_Stations/trainBetweenStations.html'
    context = {}
    context['info_page'] = "trainBetweenStations"

    """
    if request.method == "POST":
        Source_station_code = request.POST.get('Source_station_code')
        Destination_station_code = request.POST.get('Destination_station_code')
        train_date = request.POST.get('date')

        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date

        context_local ={
            'Source_station_code':Source_station_code,
            'Destination_station_code':Destination_station_code,
            'train_date':train_date,

        }

        context = get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date)

        context.update(context_local)


        return render(request,'Train_Between_Stations/trainBetweenStationsDetail.html', context)
        """

    return render(request,template_name, context)




def train_between(request):
    if request.method == "POST":
        data = {}
        print "train_between(request):"
        Source_station_code = request.POST.get('source')
        Destination_station_code = request.POST.get('dest')
        train_date = request.POST.get('date')
        Source_station_code = Source_station_code[Source_station_code.find('-')+2:]
        Destination_station_code = Destination_station_code[Destination_station_code.find('-')+2:]
        train_date = train_date[:-5]

        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date

        context = get_Train_Between_Stations_Niraj(Source_station_code,Destination_station_code,train_date)

        print "---- Return Data --------"
        return HttpResponse(json.dumps(context), content_type = "application/json")