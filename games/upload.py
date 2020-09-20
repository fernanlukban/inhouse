from games.models import *
from stats.models import *
from stats.parser.html import MatchHistory


def handle_uploaded_match_history(name, description, file):
    print(f"New game uploaded: {name} - {description}")
    with file.open() as file:
        file_contents = file.read()
        match = MatchHistory(file_contents)
        game = create_game_models(name, description, match)
        create_stat_models(game, match)
    print()


def create_game_models(name, description, match):
    game = Game(name=name, description=description)
    info = GameInfo.from_match_history(match, game=game)
    models = [game, info] + [
        *GameBanList.from_match_history_sided(match, info=info),
        *GamePickList.from_match_history_sided(match, info=info),
        *GamePlayer.from_match_history_all(match, game=game),
    ]
    for model in models:
        print(model)
        model.save()
    return game


def create_stat_models(game, match):
    stat = GameStat(game=game)
    models = [stat] + [
        *GameCombatStat.from_match_history_sided(match, game_stat=stat),
        *GameDamageStat.from_match_history_sided(match, game_stat=stat),
        *GameWardStat.from_match_history_sided(match, game_stat=stat),
        *GameIncomeStat.from_match_history_sided(match, game_stat=stat),
    ]
    for model in models:
        print(model)
        model.save()
