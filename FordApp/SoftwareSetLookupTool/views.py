from django.shortcuts import render
from FordApp.forms import BuildUrlForm,LoginForm
def login(request):
    if request.method=="GET":
        form=LoginForm()
    return render(request, "login.html")

def buildurl(request):
    if request.method=="GET":
        form=BuildUrlForm()
    else:
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            buildurl=form.cleaned_data['build_url']
    return render(request,"buildurl.html",{"Url":buildurl})

def lookuptable(request):
    return render(request, "lookuptable.html")