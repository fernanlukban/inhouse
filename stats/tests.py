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
        self.game_stat = GameStat(game=self.game)

    def test_combat_stat_kills(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.kills, [4, 4, 1, 1, 1])
        self.assertEqual(red_combat.kills, [8, 9, 1, 15, 4])

    def test_combat_stat_deaths(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.deaths, [8, 7, 9, 7, 6])
        self.assertEqual(red_combat.deaths, [0, 6, 0, 0, 5])

    def test_combat_stat_assists(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.assists, [5, 3, 5, 1, 2])
        self.assertEqual(red_combat.assists, [23, 10, 28, 11, 13])

    def test_combat_stat_largest_killing_sprees(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.largest_killing_sprees, [2, 2, 1, 1, 1])
        self.assertEqual(red_combat.largest_killing_sprees, [8, 3, 1, 15, 2])

    def test_combat_stat_largest_multi_kills(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.largest_multi_kills, [1, 1, 1, 1, 1])
        self.assertEqual(red_combat.largest_multi_kills, [2, 3, 1, 3, 1])

    def test_combat_stat_first_blood(self):
        blue_combat, red_combat = GameCombatStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_combat.first_blood, 0)
        self.assertEqual(red_combat.first_blood, 2)