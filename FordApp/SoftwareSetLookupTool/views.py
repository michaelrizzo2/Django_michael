from django.shortcuts import render
def login(request):
    return render(request, "login.html")

def buildurl(request):
    print(request)
    return render(request, "buildurl.html")

def lookuptable(request):
    print(request)
    return render(request, "lookuptable.html")