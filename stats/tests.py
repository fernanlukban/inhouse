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

    def test_damage_stat_total_damage_to_champs(self):
        blue_damage, red_damage = GameDamageStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(
            blue_damage.total_damage_to_champs, [13100, 11000, 4000, 7100, 11200]
        )
        self.assertEqual(
            red_damage.total_damage_to_champs, [13400, 16100, 5700, 33300, 14900]
        )

    def test_ward_stat_wards_placed(self):
        blue_wards, red_wards = GameWardStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_wards.wards_placed, [4, 6, 12, 10, 9])
        self.assertEqual(red_wards.wards_placed, [11, 8, 15, 6, 5])

    def test_ward_stat_wards_destroyed(self):
        blue_wards, red_wards = GameWardStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_wards.wards_destroyed, [4, 3, 8, 0, 0])
        self.assertEqual(red_wards.wards_destroyed, [3, 1, 8, 1, 3])

    def test_ward_stat_control_wards_purchased(self):
        blue_wards, red_wards = GameWardStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_wards.control_wards_purchased, [1, 2, 1, 2, 2])
        self.assertEqual(red_wards.control_wards_purchased, [3, 1, 4, 0, 3])

    def test_income_stat_gold_earned(self):
        blue_income, red_income = GameIncomeStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_income.gold_earned, [11000, 9300, 5800, 7800, 7400])
        self.assertEqual(red_income.gold_earned, [11800, 11700, 7600, 14400, 10700])

    def test_income_stat_gold_spent(self):
        blue_income, red_income = GameIncomeStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_income.gold_spent, [10800, 9000, 5300, 7300, 7200])
        self.assertEqual(red_income.gold_spent, [10800, 10200, 5500, 10100, 10300])

    def test_income_stat_minions_killed(self):
        blue_income, red_income = GameIncomeStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_income.minions_killed, [37, 168, 29, 162, 150])
        self.assertEqual(red_income.minions_killed, [176, 160, 32, 211, 20])

    def test_income_stat_neutral_minions_killed(self):
        blue_income, red_income = GameIncomeStat.from_match_history_sided(
            self.match, game_stat=self.game_stat
        )
        self.assertEqual(blue_income.neutral_minions_killed, [136, 3, 0, 8, 0])
        self.assertEqual(red_income.neutral_minions_killed, [8, 12, 0, 4, 177])