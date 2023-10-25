from django.shortcuts import render
from FordApp.forms import BuildUrlForm,LoginForm
def login(request):
    if request.method=="GET":
        form=LoginForm()
    return render(request, 'login.html', {'form': form })

def buildurl(request):
    if request.method =="GET":
        print(request)
        form=BuildUrlForm()
        print(form)
    else:
        if form.is_valid():
            print ("Success")
        print(request)
        form = BuildUrlForm()
        print(form)
    return render(request,"buildurl.html",{'form': form})

def lookuptable(request):
    return render(request, "lookuptable.html")