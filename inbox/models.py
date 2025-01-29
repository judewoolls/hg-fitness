from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coach')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    
    def __str__(self):
        return f"Chat {self.chat_id}"


class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='related_chat')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message {self.message_id}"