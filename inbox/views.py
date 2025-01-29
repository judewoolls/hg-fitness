from django.shortcuts import render

# Create your views here.
def render_inbox(request):
    return render(request, 'inbox/index.html')