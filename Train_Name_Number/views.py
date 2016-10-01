from django.shortcuts import render
from userpanal.pnr_utils import get_train_Name_Number_Niraj


def trainNameNumber(request):
    template_name = 'Train_Name_Number/trainNameNumber.html'
    context = {}

    if request.method == "POST":
        train_Name_Number = request.POST.get('trainno')
        print "train_Name_Number=%s" %train_Name_Number
        context = get_train_Name_Number_Niraj(train_Name_Number)
        return render(request,'Train_Name_Number/trainNameNumberDetail.html', context)

    return render(request,template_name, context)
