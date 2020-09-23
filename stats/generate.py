from games.models import *
from stats.models import *
from collections import OrderedDict

USERNAME = "Username"
WINS = "W"
LOSSES = "L"
TOTAL_GAMES = "Total Games"
WIN_RATE_PCT = "WR%"
KILLS = "Kills"
DEATHS = "Deaths"
ASSISTS = "Assists"
AVG_KILLS_PER_GAME = "avKPG"
AVG_DEATHS_PER_GAME = "avDPG"
AVG_ASSISTS_PER_GAME = "avAPG"
KDA = "KDA"
KILL_PCT = "KP%"
G_PCT = "G%"

HEADERS = [
    USERNAME,
    WINS,
    LOSSES,
    TOTAL_GAMES,
    WIN_RATE_PCT,
    KILLS,
    DEATHS,
    ASSISTS,
    AVG_KILLS_PER_GAME,
    AVG_DEATHS_PER_GAME,
    AVG_ASSISTS_PER_GAME,
    KDA,
    KILL_PCT,
    G_PCT,
]

stats_dict = {
    WINS: 0,
    LOSSES: 0,
    TOTAL_GAMES: 0,
    WIN_RATE_PCT: 0,
    KILLS: 0,
    DEATHS: 0,
    ASSISTS: 0,
    AVG_KILLS_PER_GAME: 0,
    AVG_DEATHS_PER_GAME: 0,
    AVG_ASSISTS_PER_GAME: 0,
    KDA: 0,
    KILL_PCT: 0,
    G_PCT: 0,
}


def generate_stats(player):
    stats = OrderedDict(stats_dict)

    game_players = GamePlayer.objects.filter(player=player)
    total_kills_for_team = 0
    total_gold_for_team = 0
    total_gold = 0
    for game_player in game_players:
        game = game_player.game
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
        stats[TOTAL_GAMES] += 1

        # SETS GAMES WON
        if (
            game_player.is_blue_side
            and info.winner == "blue"
            or not game_player.is_blue_side
            and info.winner == "red"
        ):
            stats[WINS] += 1
        else:
            stats[LOSSES] += 1

        # SETS KDA STUFF
        player_combat_stats = combat.get_stats(game_player.pick_order)
        stats[KILLS] += player_combat_stats["kills"]
        stats[DEATHS] += player_combat_stats["deaths"]
        stats[ASSISTS] += player_combat_stats["assists"]
        total_kills_for_team += sum(combat.kills)

        # SETS GOLD%
        total_gold += income.gold_earned[game_player.pick_order]
        total_gold_for_team += sum(income.gold_earned)

    # SETS WR
    stats[WIN_RATE_PCT] = f"{stats[WINS] / max(1, stats[TOTAL_GAMES])*100: 2.1f}%"

    # SETS AVERAGE KDA STUFF
    stats[AVG_KILLS_PER_GAME] = f"{stats[KILLS] / max(1, stats[TOTAL_GAMES]): 2.1f}"
    stats[AVG_DEATHS_PER_GAME] = f"{stats[DEATHS] / max(1, stats[TOTAL_GAMES]): 2.1f}"
    stats[AVG_ASSISTS_PER_GAME] = f"{stats[ASSISTS] / max(1, stats[TOTAL_GAMES]): 2.1f}"

    # SETS KDA STUFF
    stats[KDA] = f"{(stats[KILLS] + stats[ASSISTS]) / max(1, stats[DEATHS]): 2.1f}"

    # SETS KP%
    stats[
        KILL_PCT
    ] = f"{(stats[KILLS] + stats[ASSISTS]) / max(1, total_kills_for_team)*100: 2.1f}%"

    # SETS G%
    stats[G_PCT] = f"{total_gold / total_gold_for_team*100: 2.1f}%"

    return stats