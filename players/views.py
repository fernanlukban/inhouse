from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Player

# Create your views here.
def index(request):
    return HttpResponse("Hello")

def view_player(request, username):
    try:
        player = Player.objects.get(username=username)
    except Player.DoesNotExist:
        raise Http404(f"Player: {username} does not exist")
    return HttpResponse(f"{player}")