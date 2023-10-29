from django.shortcuts import render
from FordApp.forms import BuildUrlForm,LoginForm
def login(request):
    print(request.method)
    if request.method =="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            print("Success")
            print(form)
    else:
        form=LoginForm()


    return render(request, 'buildurl.html', {'form': form })



def buildurl(request):
    if request.method =="POST":
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            print("Success")
            print(form)
    else:
        form=BuildUrlForm()

    return render(request,"lookuptable.html",{'form': form})

def lookuptable(request):
    return render(request, "lookuptable.html")