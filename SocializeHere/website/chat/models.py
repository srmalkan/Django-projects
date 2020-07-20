from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class contact(models.Model):
    user = models.ForeignKey(User, related_name="friends", on_delete=models.CASCADE)    
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse("contact_detail", kwargs={"pk": self.pk})


class Message(models.Model):
    contact = models.ForeignKey(contact,related_name="messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class chat(models.Model):
    participants = models.ManyToManyField(contact,related_name='chats')
    messages = models.ManyToManyField(Message)
    room_name = models.CharField(max_length=50 , default='test')
    slug = models.SlugField(default="test")

    def last_message(self):
        return self.messages.order_by('-timestamp').all()[0]

    def last_10_messages(self):
        print("in")
        return self.messages.objects.order_by('-timestamp').all()[:10]

    def get_absolute_url(self):
        return reverse("chat:room", kwargs={"room_name": self.slug})
    