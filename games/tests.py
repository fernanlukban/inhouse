from django.test import TestCase
from .models import Game, GameInfo, GameBanList, GamePickList, GamePlayer
from stats.parser.html import MatchHistory

# Create your tests here.
class GameModels(TestCase):
    def setUp(self):
        self.match = MatchHistory.from_file(
            "/mnt/c/Users/Fernan Lukban/Documents/inhouse/stats/parser/Match History Complete.html"
        )
        self.game = Game()

    def test_game_info_from_match_history(self):
        game_info = GameInfo.from_match_history(self.match)
        self.assertEqual(game_info.winner, "red")

    def test_game_ban_list_from_match_history(self):
        info = GameInfo.from_match_history(self.match, game=self.game)
        blue_bans, red_bans = GameBanList.from_match_history_sided(
            self.match, info=info
        )
        self.assertEqual(
            blue_bans.bans, ["Akali", "Blitzcrank", "Annie", "Ashe", "Senna"]
        )
        self.assertEqual(
            red_bans.bans,
            ["Evelynn", "Karthus", "Talon", "Nidalee", "Kayle"],
        )

    def test_game_pick_list_from_match_history(self):
        info = GameInfo.from_match_history(self.match, game=self.game)
        blue_picks, red_picks = GamePickList.from_match_history_sided(
            self.match, info=info
        )
        self.assertEqual(
            blue_picks.picks,
            ["MasterYi", "Riven", "Thresh", "Caitlyn", "Syndra"],
        )
        self.assertEqual(
            red_picks.picks, ["Lulu", "Fiora", "Rakan", "Ezreal", "Hecarim"]
        )

    def test_game_player_from_match_history_all_player(self):
        players = GamePlayer.from_match_history_all(self.match, game=self.game)
        blue_players, red_players = players[:5], players[5:]
        self.assertEqual(
            [player.player.username for player in blue_players],
            ["FruitSmoothie27", "Shinigámí", "Koó", "enwards", "Vassallo"],
        )
        self.assertEqual(
            [player.player.username for player in red_players],
            ["fk the system", "Chicago Boy", "Espia", "KeIlen", "opsadboys"],
        )

    def test_game_player_from_match_history_all_blue_side(self):
        players = GamePlayer.from_match_history_all(self.match, game=self.game)
        blue_players, red_players = players[:5], players[5:]
        self.assertEqual(
            [player.is_blue_side for player in blue_players], [True for i in range(5)]
        )
        self.assertEqual(
            [player.is_blue_side for player in red_players], [False for i in range(5)]
        )

    def test_game_player_from_match_history_all_champion(self):
        players = GamePlayer.from_match_history_all(self.match, game=self.game)
        blue_players, red_players = players[:5], players[5:]
        self.assertEqual(
            [player.champion for player in blue_players],
            ["MasterYi", "Riven", "Thresh", "Caitlyn", "Syndra"],
        )
        self.assertEqual(
            [player.champion for player in red_players],
            ["Lulu", "Fiora", "Rakan", "Ezreal", "Hecarim"],
        )
