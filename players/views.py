from django.shortcuts import render
from django.http import HttpResponse, Http404
from stats.generate import generate_stats, HEADERS

from .models import Player
from games.models import *
from stats.generate import *
from stats.models import *
from collections import OrderedDict
from .forms import DuoForm

# Create your views here.


def index(request):
    stats = {}
    for player in Player.objects.all():
        aggregated_stats[player.username][player.username] = generate_stats(player)
    return render(request, "players/index.html", {"stats": stats, "headers": HEADERS})


def view_player(request, username):
    try:
        player = Player.objects.get(username=username)
    except Player.DoesNotExist:
        raise Http404(f"Player: {username} does not exist")
    return HttpResponse(f"{player}")


def generate_duo_stats(username1, username2):
    if username1 == username2:
        raise Http404(
            f"You entered {username1} twice, please choose different summoners"
        )
    try:
        player1 = Player.objects.get(username=username1)
        player2 = Player.objects.get(username=username2)
    except Player.DoesNotExist:
        raise Http404(f"Players: {username1}  or {username2} does not exist")

    player1_games = set(
        [gameplayer.game for gameplayer in GamePlayer.objects.filter(player=player1)]
    )
    player2_games = set(
        [gameplayer.game for gameplayer in GamePlayer.objects.filter(player=player2)]
    )
    intersection_games = player1_games.intersection(player2_games)

    aggregated_stats = {
        player1.username: OrderedDict(stats_dict),
        player2.username: OrderedDict(stats_dict),
    }

    for player in (player1, player2):
        total_kills_for_team = 0
        total_gold_for_team = 0
        total_gold = 0
        for game in intersection_games:
            game_player = GamePlayer.objects.filter(player=player).get(game=game)
            info = GameInfo.objects.get(game=game)
            stat = GameStat.objects.get(game=game)
            combat = GameCombatStat.objects.get(
                game_stat=stat, is_blue_side=game_player.is_blue_side
            )
            damage = GameDamageStat.objects.get(
                game_stat=stat, is_blue_side=game_player.is_blue_side
            )
            ward = GameWardStat.objects.get(
                game_stat=stat, is_blue_side=game_player.is_blue_side
            )
            income = GameIncomeStat.objects.get(
                game_stat=stat, is_blue_side=game_player.is_blue_side
            )

            # SETS GAMES PLAYED
            aggregated_stats[player.username][TOTAL_GAMES] += 1

            # SETS GAMES WON
            if (
                game_player.is_blue_side
                and info.winner == "blue"
                or not game_player.is_blue_side
                and info.winner == "red"
            ):
                aggregated_stats[player.username][WINS] += 1
            else:
                aggregated_stats[player.username][LOSSES] += 1

            # SETS KDA STUFF
            player_combat_stats = combat.get_stats(game_player.pick_order)
            aggregated_stats[player.username][KILLS] += player_combat_stats["kills"]
            aggregated_stats[player.username][DEATHS] += player_combat_stats["deaths"]
            aggregated_stats[player.username][ASSISTS] += player_combat_stats["assists"]
            total_kills_for_team += sum(combat.kills)

            # SETS GOLD%
            total_gold += income.gold_earned[game_player.pick_order]
            total_gold_for_team += sum(income.gold_earned)
        # SETS WR
        aggregated_stats[player.username][
            WIN_RATE_PCT
        ] = f"{aggregated_stats[player.username][WINS] / max(1, aggregated_stats[player.username][TOTAL_GAMES])*100: 2.1f}%"

        # SETS AVERAGE KDA STUFF
        aggregated_stats[player.username][
            AVG_KILLS_PER_GAME
        ] = f"{aggregated_stats[player.username][KILLS] / max(1, aggregated_stats[player.username][TOTAL_GAMES]): 2.1f}"
        aggregated_stats[player.username][
            AVG_DEATHS_PER_GAME
        ] = f"{aggregated_stats[player.username][DEATHS] / max(1, aggregated_stats[player.username][TOTAL_GAMES]): 2.1f}"
        aggregated_stats[player.username][
            AVG_ASSISTS_PER_GAME
        ] = f"{aggregated_stats[player.username][ASSISTS] / max(1, aggregated_stats[player.username][TOTAL_GAMES]): 2.1f}"

        # SETS KDA STUFF
        aggregated_stats[player.username][
            KDA
        ] = f"{(aggregated_stats[player.username][KILLS] + aggregated_stats[player.username][ASSISTS]) / max(1, aggregated_stats[player.username][DEATHS]): 2.1f}"

        # SETS KP%
        aggregated_stats[player.username][
            KILL_PCT
        ] = f"{(aggregated_stats[player.username][KILLS] + aggregated_stats[player.username][ASSISTS]) / max(1, total_kills_for_team)*100: 2.1f}%"

        # SETS G%
        aggregated_stats[player.username][
            G_PCT
        ] = f"{total_gold / total_gold_for_team*100: 2.1f}%"
    return aggregated_stats


def view_duo(request, username1, username2):
    aggregated_stats = generate_duo_stats(username1, username2)
    return render(
        request, "players/index.html", {"stats": aggregated_stats, "headers": HEADERS}
    )


def select_duo(request):
    if request.method == "POST":
        form = DuoForm(request.POST)
        print(form.data)
        if form.is_valid():
            aggregated_stats = generate_duo_stats(
                form.data["username1"], form.data["username2"]
            )
            return render(
                request,
                "players/duo.html",
                {"stats": aggregated_stats, "headers": HEADERS, "form": form},
            )
        else:
            print("not valid")
    else:
        form = DuoForm()
    return render(request, "players/duo.html", {"form": form})
