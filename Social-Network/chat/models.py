from django.db import models
from profiles.models import Profile
from datetime import datetime

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)
class Messenge(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chats')
    room = models.CharField(max_length=1000000)
    nameuser = models.CharField(max_length=1000000, null=True)
    imgUrl  = models.CharField(max_length=1000000,null= True )
    def __str__(self):
        return f"{self.value}-{self.date.strftime('%d-%m-%Y')}"