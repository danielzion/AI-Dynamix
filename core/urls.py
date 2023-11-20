from django.urls import path, include
from .views import *


app_name = 'core'

urlpatterns = [
    path('codehub', codehub, name='codehub'),
    path('automate', automate, name='automate'),
    path('tester', tester, name='tester'),
    path('result/<str:category>/<int:pk>', result, name='result'),
]