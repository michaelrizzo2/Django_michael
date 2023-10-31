from django.shortcuts import render,redirect
from FordApp.forms import BuildUrlForm


def buildurl(request):
    if request.method =="POST":
        form=BuildUrlForm(request.POST)
        if form.is_valid():
            build_url=form.cleaned_data['build_url']
            return redirect('lookuptable',build_url=build_url)
    else:
        form=BuildUrlForm()
    return render(request,"buildurl.html",{'form': form})

def lookuptable(request,build_url):
    print(request.method)
    my_variable = request.GET.get('build_url')
    context = {'my_variable': build_url}
    return render(request, 'lookuptable.html', context)
    if request.method=="GET":
        print(request)
    return render(request,"lookuptable.html",{"data": build_url})