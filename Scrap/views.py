from django.shortcuts import render,HttpResponse


#Custom Functions Here

# Create your views here.
def index(request):
    return HttpResponse("Home Page of Medium Scrapper")
