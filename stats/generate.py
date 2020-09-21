from games.models import *
from stats.models import *
from collections import OrderedDict


def generate_stats(player):
    stats = OrderedDict(
        {
            "Games Played": 0,
            "Games Won": 0,
            "Average Kills": 0,
            "Average Deaths": 0,
            "Average Assists": 0,
            "KDA": 0,
        }
    )
    game_players = GamePlayer.objects.filter(player=player)
    for game_player in game_players:
        # SETS GAMES PLAYED
        stats["Games Played"] += 1
        game = game_player.game
        info = GameInfo.objects.get(game=game)

        # SETS GAMES WON
        if (
            game_player.is_blue_side
            and info.winner == "blue"
            or not game_player.is_blue_side
            and info.winner == "red"
        ):
            stats["Games Won"] += 1

        stat = GameStat.objects.get(game=game)
        combat = GameCombatStat.objects.get(
            game_stat=stat, is_blue_side=game_player.is_blue_side
        )

        # SETS KDA STUFF
        stats["Average Kills"] += combat.kills[game_player.pick_order]
        stats["Average Deaths"] += combat.deaths[game_player.pick_order]
        stats["Average Assists"] += combat.assists[game_player.pick_order]

        damage = GameDamageStat.objects.get(
            game_stat=stat, is_blue_side=game_player.is_blue_side
        )
        ward = GameWardStat.objects.get(
            game_stat=stat, is_blue_side=game_player.is_blue_side
        )
        income = GameIncomeStat.objects.get(
            game_stat=stat, is_blue_side=game_player.is_blue_side
        )
    total_kills = stats["Average Kills"]
    total_assists = stats["Average Assists"]
    total_deaths = stats["Average Deaths"]
    kda_divisor = 1 if total_deaths == 0 else total_deaths
    stats["KDA"] = f"{(total_kills + total_assists)/kda_divisor:.2f}"
    games_divisor = stats["Games Played"] if stats["Games Played"] != 0 else 1
    stats["Average Kills"] /= games_divisor
    stats["Average Deaths"] /= games_divisor
    stats["Average Assists"] /= games_divisor
    stats["Total Kills"] = total_kills
    stats["Total Deaths"] = total_deaths
    stats["Total Assists"] = total_assists
    wr = stats["Games Won"] / max(stats["Games Played"], 1)
    stats["WR%"] = f"{wr*100:.2f}%"

    return stats