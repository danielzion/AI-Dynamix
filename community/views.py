from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Room, Message

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'community/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messag = Message.objects.filter(room=room).order_by('-date_added')[0:25][::-1]

    return render(request, 'community/room.html', {'room': room, 'messag': messag})