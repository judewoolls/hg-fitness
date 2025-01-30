from django.shortcuts import render, redirect
from .models import Chat, Message
from .forms import MessageForm

# Create your views here.
def render_inbox(request):
    chats = Chat.objects.filter(coach=request.user) | Chat.objects.filter(user=request.user)
    return render(request, 'inbox/index.html', {'chats': chats})

def render_chat(request, chat_id):
    chat = Chat.objects.get(chat_id=chat_id)
    messages = Message.objects.filter(chat_id=chat)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            Message.objects.create(
                sender=request.user,
                chat_id=chat,
                body=message
            )
            return redirect('chat', chat_id=chat_id)
    else:
        form = MessageForm()
    
    return render(request, 'inbox/chat.html', {'chat': chat, 'messages': messages, 'form': form})