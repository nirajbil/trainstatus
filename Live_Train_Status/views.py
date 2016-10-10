from django.shortcuts import render
from userpanal.pnr_utils import get_train_live_status_Niraj
import datetime
from django.http import HttpResponse
import json
# Create your views here.


def liveTrainStatus(request):
    template_name = 'Live_Train_Status/liveTrainStatus.html'
    context = {'request': request,'user': request.user}
    return render(request,template_name, context)




def live_train_status_detail(request):
    if request.method == "POST":
        train_no = request.POST.get('trainNumber')
        now = datetime.datetime.now()
        train_date = "%04s%02s%02s" % (str(now.year),str(now.month).zfill(2),str(now.day).zfill(2))
        #train_date = '20160925'
        print "train_no=%s train_date=%s" %(train_no, train_date)
        context = get_train_live_status_Niraj(train_no,train_date)
        print "--- return data live_train_status_detail-----"
        return HttpResponse(json.dumps(context), content_type = "application/json")