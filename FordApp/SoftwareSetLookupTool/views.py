from django.shortcuts import render
from FordApp.forms import BuildUrlForm


def buildurl(request):
    if request.method =="POST":
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            print("Success")
            print(form)
        return render(request,"buildurl.html",{'form': form})
    else:
        form=BuildUrlForm()

    return render(request,"buildurl.html",{'form': form})

def lookuptable(request):
    pass
    return render(request,"lookuptable.html")