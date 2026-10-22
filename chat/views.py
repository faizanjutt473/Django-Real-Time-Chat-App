from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    old_messages = Message.objects.filter(room=room_name).select_related("user")
    chat_history = [
        {
            "username": m.user.username if m.user else "Unknown",
            "message": m.content,
        }
        for m in old_messages
    ]
    return render(request, "chat/room.html", {
        "room_name": room_name,
        "chat_history": chat_history,
    })
    
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})    