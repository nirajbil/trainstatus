from django.shortcuts import render
from userpanal.pnr_utils import get_train_route_Niraj
from django.http import HttpResponse
import json

def trainRoute(request):
    template_name = 'Train_Route/trainRoute.html'
    context = {}

    return render(request,template_name, context)

def train_Route_detail(request):
    if request.method == "POST":
        train_no = request.POST.get('trainNumber')
        print "train_no=%s" %train_no
        context = get_train_route_Niraj(train_no)
        return HttpResponse(json.dumps(context), content_type = "application/json")

