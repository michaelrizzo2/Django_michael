from django.shortcuts import render
def home(request):
    return render(request, "login.html")

def projects(request):
    return render(request, "buildurl.html")

def contact(request):
    return render(request, "lookuptable.html")