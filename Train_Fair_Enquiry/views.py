from django.shortcuts import render
from userpanal.pnr_utils import get_Train_Fair_Enquiry_Niraj


def trainFairEnquiry(request):
    template_name = 'Train_Fair_Enquiry/trainFairEnquiry.html'
    context = {}


    if request.method == "POST":
        trainno = request.POST.get('trainno')
        Source_station_code = request.POST.get('Source_station_code')
        Destination_station_code = request.POST.get('Destination_station_code')
        Age_of_the_passenger = request.POST.get('Age_of_the_passenger')
        train_quota = request.POST.get('train_quota')
        train_date = request.POST.get('date')

        print "Age_of_the_passenger=%s" %Age_of_the_passenger
        print "trainno=%s" %trainno
        print "Source_station_code=%s" %Source_station_code
        print "Destination_station_code=%s" %Destination_station_code
        print "train_date=%s" %train_date

        context = get_Train_Fair_Enquiry_Niraj(Source_station_code,Destination_station_code,
                                                   trainno, Age_of_the_passenger,train_quota,
                                                   train_date)
        return render(request,'Train_Fair_Enquiry/trainFairEnquiryDetail.html', context)

    return render(request,template_name, context)
