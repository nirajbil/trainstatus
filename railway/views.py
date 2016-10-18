from django.shortcuts import render




def page_not_found(request):
    print "page_not_found"
    template_name = '404.html'
    context = {}
    return render(request,template_name, context)




def permission_denied(request):
    print "permission_denied"
    template_name = '403.html'
    context = {}
    return render(request,template_name, context)


def bad_request(request):
    print "bad_request"
    template_name = '400.html'
    context = {}
    return render(request,template_name, context)

def server_error(request):
    print "server_error"
    template_name = '500.html'
    context = {}
    return render(request,template_name, context)