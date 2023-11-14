from django.urls import path

from . import views

app_name = 'community'

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),
]
