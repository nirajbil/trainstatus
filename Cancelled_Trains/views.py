from django.shortcuts import render
from userpanal.pnr_utils import get_cancelled_Trains_Niraj
import datetime

def cancelledTrains(request):
    template_name = 'Cancelled_Trains/cancelledTrains.html'
    context = {}
    now = datetime.datetime.now()
    train_date = "%02s-%02s-%04s" % (str(now.day).zfill(2),str(now.month).zfill(2),str(now.year))

    context = get_cancelled_Trains_Niraj(train_date)

    """
    if request.method == "POST":
        train_no = request.POST.get('trainno')
        print "train_no=%s" %train_no
        context = get_train_route_Niraj(train_no)
        return render(request,'Train_Route/trainRouteDetail.html', context)
    """

    return render(request,template_name, context)