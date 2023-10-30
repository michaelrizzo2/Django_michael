from django.shortcuts import render
from FordApp.forms import BuildUrlForm


def buildurl(request):
    print(request.method)
    if request.method =="POST":
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            print("Success")
            print(form.cleaned_data["build_url"])
        return render(request,"buildurl.html",{'form': form})
    else:
        form=BuildUrlForm()

    return render(request,"buildurl.html",{'form': form})

def lookuptable(request):
    return render(request,"lookuptable.html")