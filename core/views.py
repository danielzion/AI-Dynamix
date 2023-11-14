from django.shortcuts import render, redirect


# Create your views here.
def codehub(request):
    
    return render(request, 'codehub.html')

def automate(request):
    
    return render(request, 'automate.html')

def tester(request):
    
    return render(request, 'tester.html')