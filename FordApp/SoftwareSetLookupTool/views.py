from django.shortcuts import render
from FordApp.forms import BuildUrlForm


def buildurl(request):
    print(request.method)
    if request.method =="GET":
        form=BuildUrlForm(request.GET)
        if form.is_valid():
            print("Success")
        return render(request,"buildurl.html",{'form': form})
    else:
        form=BuildUrlForm(request.POST)
    return render(request,"buildurl.html",{'form': form})

def lookuptable(request):
    return render(request,"lookuptable.html")