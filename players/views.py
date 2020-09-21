from django.shortcuts import render
from django.http import HttpResponse, Http404
from stats.generate import generate_stats, HEADERS

from .models import Player

# Create your views here.


def index(request):
    stats = {}
    for player in Player.objects.all():
        stats[player.username] = generate_stats(player)
    return render(request, "players/index.html", {"stats": stats, "headers": HEADERS})


def view_player(request, username):
    try:
        player = Player.objects.get(username=username)
    except Player.DoesNotExist:
        raise Http404(f"Player: {username} does not exist")
    return HttpResponse(f"{player}")
