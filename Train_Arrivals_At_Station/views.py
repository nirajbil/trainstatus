from django.shortcuts import render
from userpanal.pnr_utils import get_train_Arrivals_At_Station_Niraj


def trainArrivalsAtStation(request):
    template_name = 'Train_Arrivals_At_Station/trainArrivalsAtStation.html'
    context = {}

    if request.method == "POST":
        stationCode = request.POST.get('stationCode')
        print "stationCode=%s" %stationCode
        context = get_train_Arrivals_At_Station_Niraj(stationCode)
        return render(request,'Train_Arrivals_At_Station/trainArrivalsAtStationDetail.html', context)

    return render(request,template_name, context)
