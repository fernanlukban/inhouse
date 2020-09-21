from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import MatchHistoryFileFieldForm
from .upload import handle_uploaded_match_history
from .models import *

# Create your views here.
def upload_match_history(request):
    if request.method == "POST":
        form = MatchHistoryFileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_match_history(
                form.data["name"],
                form.data["description"],
                request.FILES["match_history_file"],
            )
            return HttpResponseRedirect(reverse("games:show_games"))
        else:
            print("not valid")
    else:
        form = MatchHistoryFileFieldForm()
    return render(request, "games/upload.html", {"form": form})


def show_games(request):
    games = Game.objects.all()
    players = []
    for game in games:
        blue_players = GamePlayer.objects.filter(game=game).filter(is_blue_side=True)
        red_players = GamePlayer.objects.filter(game=game).filter(is_blue_side=False)
        blue_red_pairs = zip(
            [game_player.player for game_player in blue_players],
            [game_player.player for game_player in red_players],
        )
        players.append(blue_red_pairs)
    games_and_players = zip(games, players)
    return render(request, "games/index.html", {"games_and_players": games_and_players})
