"""
URL configuration for hgfitness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from homepage.views import home
from booking.views import booking
from feedback.views import feedback, diet
from inbox.views import render_inbox, render_chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('booking/', include('booking.urls'), name='booking-urls'),
    path('feedback/', feedback, name='feedback'),
    path('inbox/', render_inbox, name='inbox'),
    path('inbox/view_chat/<int:chat_id>', render_chat, name='chat'),
    path('diet/', diet, name='diet'),
    path('', home, name='home'),
]
