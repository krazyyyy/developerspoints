from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.forms import model_to_dict
from django.contrib import messages

from .models import ProjectImages, Portfolio, Contact, EmailLists
# Create your views here.
def index(request):
    return render(request, 'frontend/index.html')

def portfolio(request):
    return render(request, 'frontend/portfolio.html')

def about(request):
    return render(request, 'frontend/about.html')

def services(request):
    return render(request, 'frontend/services.html')

def contact(request):
    return render(request, 'frontend/contact.html')

def single_portfolio(request, pk):
    profile = Portfolio.objects.get(id=pk)
    return render(request, 'frontend/single-portfolio.html', {
        "profile" : profile
    })

def getProfiles(request):
    profiles = Portfolio.objects.all()
    li = []
    for i in profiles:
        prof = model_to_dict(i)
        prof.pop("image", None)
        prof.pop("project_picture", None)
        try:
            prof['img_link'] = i.image.url
        except:
            prof['img_link'] = ""

        li.append(prof)
    profile = dict(profile=li)
    return JsonResponse(profile)

def contactResponse(request):
    email = request.POST.get('email') 
    name = request.POST.get('name') 
    message = request.POST.get('message')
    try:
        emails = EmailLists.object.get(email=email)
    except:
        emails = EmailLists(email=email)
        emails.save()
    contact = Contact(email=emails, name=name, message=message)
    contact.save()
    messages.error(request, "Message Succesfully Sent.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 