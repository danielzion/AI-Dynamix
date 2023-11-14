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

def gallery(request):
    
    return render(request, 'gallery.html')

def services(request):
    
    return render(request, 'services.html')