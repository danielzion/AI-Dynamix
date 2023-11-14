from django.urls import path, include
from .views import *

urlpatterns = [
    path('codehub', codehub, name='codehub'),
    path('automate', automate, name='automate'),
    path('tester', tester, name='tester'),
]