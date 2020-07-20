from django.shortcuts import render
from .models import Message, contact, chat

# Create your views here.
def index(request):
    user = request.user
    cont= contact.objects.get(user=user)
    chats = cont.chats.all()
    context= {
        'chats':chats
    }
    # if slug is not None:
    #     context['room_name']=slug
    return render(request, 'chat/index.html',context)

def room(request, room_name):
    user = request.user
    cont= contact.objects.get(user=user)
    chats = cont.chats.all()
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username':request.user.username,
        'chats':chats
    })