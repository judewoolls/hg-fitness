from django.shortcuts import render
from .models import Chat, Message

# Create your views here.
def render_inbox(request):
    chats = Chat.objects.filter(coach=request.user) | Chat.objects.filter(user=request.user)
    return render(request, 'inbox/index.html', {'chats': chats})

def render_chat(request):
    chat = Chat.objects.get(chat_id=1)
    messages = Message.objects.filter(chat_id=chat)
    return render(request, 'inbox/chat.html', {'chat': chat, 'messages': messages})