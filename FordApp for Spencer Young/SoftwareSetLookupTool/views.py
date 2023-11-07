from django.shortcuts import render,redirect
from FordApp.forms import BuildUrlForm
#from SoftwareSetLookupTool.swum_utils import DatabaseManager


def buildurl(request):
    if request.method =="POST":
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            build_url=form.cleaned_data['build_url']
            return lookuptable(request,build_url)
    else:
        form=BuildUrlForm()
    return render(request,"buildurl.html",{'form': form})

def lookuptable(request,build_url):
    print(request.method)
    my_variable = request.GET.get('build_url')
    context = {'my_variable': build_url}
    return render(request, 'lookuptable.html', context)