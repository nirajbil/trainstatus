from django.shortcuts import render
from userpanal.pnr_utils import get_seat_availability_Niraj


def seatAvailability(request):
    template_name = 'Seat_Availability/seatAvailability.html'
    context = {}


    if request.method == "POST":
        trainno = request.POST.get('trainno')
        Source_station_code = request.POST.get('Source_station_code')
        Destination_station_code = request.POST.get('Destination_station_code')
        train_date = request.POST.get('date')
        train_class = request.POST.get('train_class')
        train_quota = request.POST.get('train_quota')


        context = get_seat_availability_Niraj(trainno,Source_station_code,
                                              Destination_station_code,train_date,
                                              train_class,train_quota)
        return render(request,'Seat_Availability/seatAvailabilityDetail.html', context)

    return render(request,template_name, context)