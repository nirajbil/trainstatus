from django.shortcuts import render
from userpanal.pnr_utils import get_train_route_Niraj


def trainBetweenStation(request):
    template_name = 'Train_Between_Station/trainBetweenStation.html'
    context = {}

    if request.method == "POST":
        train_no = request.POST.get('trainno')
        print "train_no=%s" %train_no
        #context = get_train_route_Niraj(train_no)
        return render(request,'Train_Between_Station/trainBetweenStationDetail.html', context)

    return render(request,template_name, context)