from django.shortcuts import render, get_object_or_404
from datetime import timedelta
from datetime import datetime
from userpanal.pnr_utils import get_pnr_status_Niraj
from userpanal.models import PNRNotification, RecentPNR, UserProfile, API_Key

def Database(request):
    print "== Database =="
    context = {}
    template_name = 'Database/Database.html'
    list = []
    print "ReadDataBase request.user=%s" %request.user
    if request.user.is_authenticated:
        username = get_object_or_404(UserProfile, user=request.user)
        print "ReadDataBase username=%s" %username

        all_pnr_db = RecentPNR.objects.filter(userprofile=username)
        print "all_pnr_db=%s" %all_pnr_db

        for db in all_pnr_db:
            nowDate = datetime.now().date()
            dataBaseDate = datetime.strptime(db.DateOfJourney, '%d-%m-%Y').date()

            if dataBaseDate >= nowDate:
                list.append({'RecentPnrNo': db.RecentPnrNo,
                              'Srcdest': db.Srcdest,
                              'DateOfJourney': db.DateOfJourney,
                              })
                print "True"
            else:
                RecentPNR.objects.filter(RecentPnrNo=db.RecentPnrNo).delete()
                print "False"

        context['all_pnr_db'] = list
        context['info_page'] = "Database"
        return render(request,template_name, context)

    return render(request,template_name, context)


def pnr(request):
    print "== pnr =="
    context = {}
    template_name = 'Database/pnr.html'
    if request.method=='GET':
        pnrNo = request.GET.get('pnrNo')
        print "pnrNo=%s" %pnrNo

        context = get_pnr_status_Niraj(pnrNo)

    context['info_page'] = "index"
    return render(request,template_name, context)