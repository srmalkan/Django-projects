from django.urls import path,include,reverse_lazy
from .views import index, room

app_name = 'chat'

urlpatterns = [
    path('',index,name='index'),
    path('<str:room_name>/', room, name='room'),
]
