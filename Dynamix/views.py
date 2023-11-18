from django.shortcuts import render, redirect


# Create your views here.
def index(request):
    
    return render(request, 'index.html')

def about(request):
    
    return render(request, 'about.html')

def contact(request):
    
    return render(request, 'contact.html')

def team(request):
    
    return render(request, 'team.html')

def dynamix(request):
    
    return render(request, 'dynamix.html')

def services(request):
    
    return render(request, 'services.html')