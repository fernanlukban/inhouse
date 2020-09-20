from django.test import TestCase
from games.models import Game
from .models import (
    GameStat,
    GameCombatStat,
    GameDamageStat,
    GameWardStat,
    GameIncomeStat,
)
from stats.parser.html import MatchHistory

# Create your tests here.
class GameStatModels(TestCase):
    def setUp(self):
        self.match = MatchHistory.from_file(
            "/mnt/c/Users/Fernan Lukban/Documents/inhouse/stats/parser/Match History Complete.html"
        )
        self.game = Game()
        self.game_stat = GameStat(game=game)

    def test_combat_stat_kills(self):
        combat = GameCombatStat(game_stat=self.game_stat)