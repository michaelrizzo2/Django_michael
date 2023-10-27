from django.shortcuts import render
from FordApp.forms import BuildUrlForm,LoginForm
def login(request):
    print(request.method)
    if request.method =="GET":
        form=LoginForm()
        print(form)
    return render(request, 'login.html', {'form': form })



def buildurl(request):
    print(request.method)
    if request.method =="GET":
        form=BuildUrlForm()
        print(form)

    return render(request,"buildurl.html",{'form': form})

def lookuptable(request):
    return render(request, "lookuptable.html")