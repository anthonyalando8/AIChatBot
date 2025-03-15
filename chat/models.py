from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Chat(models.Model):
    message = models.CharField(max_length=12000)
    image = models.ImageField(upload_to="images/")

class ChatHistory(models.Model):
    user = models.ForeignKey(User, related_name="chat_history", on_delete=models.CASCADE, null=False, blank=False)
    chat_history = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Message(models.Model):
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField()
    response = models.TextField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.date)