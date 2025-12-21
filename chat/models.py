from django.db import models
from django.utils import timezone


# Create your models here.
class Room (models. Model):
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=50)  # <-- add this



    

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"
