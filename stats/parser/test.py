from .html import MatchHistory
from collections import OrderedDict
import unittest


class TestMatchHistory(unittest.TestCase):
    def setUp(self):
        self.match = MatchHistory.from_file(
            "/mnt/c/Users/Fernan Lukban/Documents/inhouse/stats/parser/Match History Complete.html"
        )

    def test_parse_bans(self):
        self.assertEqual(
            self.match.blue_side_bans, ["Akali", "Blitzcrank", "Annie", "Ashe", "Senna"]
        )
        self.assertEqual(
            self.match.red_side_bans,
            ["Evelynn", "Karthus", "Talon", "Nidalee", "Kayle"],
        )

    def test_parse_picks(self):
        self.assertEqual(
            self.match.blue_side_picks,
            ["MasterYi", "Riven", "Thresh", "Caitlyn", "Syndra"],
        )
        self.assertEqual(
            self.match.red_side_picks, ["Lulu", "Fiora", "Rakan", "Ezreal", "Hecarim"]
        )

    def test_parse_players(self):
        self.assertEqual(
            self.match.blue_side_players,
            ["FruitSmoothie27", "Shinigámí", "Koó", "enwards", "Vassallo"],
        )
        self.assertEqual(
            self.match.red_side_players,
            ["fk the system", "Chicago Boy", "Espia", "KeIlen", "opsadboys"],
        )

    def test_parse_objectives(self):
        self.assertEqual(
            self.match.blue_side_objectives,
            {
                "tower_kills": "1",
                "baron_kills": "0",
                "dragon_kills": "0",
                "rift_herald_kills": "2",
                "inhibitor_kills": "0",
            },
        )
        self.assertEqual(
            self.match.red_side_objectives,
            {
                "tower_kills": "9",
                "baron_kills": "0",
                "dragon_kills": "4",
                "rift_herald_kills": "0",
                "inhibitor_kills": "1",
            },
        )

    def test_parse_winner(self):
        self.assertEqual(self.match.winner, "red")

    def test_parse_stats(self):
        self.assertEqual(
            self.match.stats,
            OrderedDict(
                [
                    (
                        "KDA",
                        [
                            "4/8/5",
                            "4/7/3",
                            "1/9/5",
                            "1/7/1",
                            "1/6/2",
                            "8/0/23",
                            "9/6/10",
                            "1/0/28",
                            "15/0/11",
                            "4/5/13",
                        ],
                    ),
                    (
                        "Largest Killing Spree",
                        ["2", "2", "1", "1", "1", "8", "3", "1", "15", "2"],
                    ),
                    (
                        "Largest Multi Kill",
                        ["1", "1", "1", "1", "1", "2", "3", "1", "3", "1"],
                    ),
                    ("First Blood", ["○", "○", "○", "○", "○", "○", "●", "○", "○", "○"]),
                    (
                        "Total Damage to Champions",
                        [
                            "13.1k",
                            "11.0k",
                            "4.0k",
                            "7.1k",
                            "11.2k",
                            "13.4k",
                            "16.1k",
                            "5.7k",
                            "33.3k",
                            "14.9k",
                        ],
                    ),
                    (
                        "Physical Damage to Champions",
                        [
                            "8.5k",
                            "10.7k",
                            "0.4k",
                            "6.7k",
                            "0.5k",
                            "1.3k",
                            "12.1k",
                            "1.2k",
                            "18.1k",
                            "10.7k",
                        ],
                    ),
                    (
                        "Magic Damage to Champions",
                        [
                            "0.6k",
                            "0.0k",
                            "3.5k",
                            "0.4k",
                            "10.5k",
                            "12.0k",
                            "0.8k",
                            "4.0k",
                            "13.2k",
                            "2.2k",
                        ],
                    ),
                    (
                        "True Damage to Champions",
                        [
                            "4.0k",
                            "0.2k",
                            "0.1k",
                            "0.0k",
                            "0.1k",
                            "0.1k",
                            "3.3k",
                            "0.5k",
                            "2.0k",
                            "2.0k",
                        ],
                    ),
                    (
                        "Total Damage Dealt",
                        [
                            "168.0k",
                            "92.8k",
                            "12.1k",
                            "84.8k",
                            "82.5k",
                            "97.3k",
                            "125.7k",
                            "21.6k",
                            "148.8k",
                            "188.9k",
                        ],
                    ),
                    (
                        "Physical Damage Dealt",
                        [
                            "135.0k",
                            "85.4k",
                            "2.4k",
                            "79.7k",
                            "9.8k",
                            "15.4k",
                            "106.7k",
                            "8.3k",
                            "114.7k",
                            "149.3k",
                        ],
                    ),
                    (
                        "Magic Damage Dealt",
                        [
                            "7.6k",
                            "0.0k",
                            "6.4k",
                            "0.8k",
                            "70.0k",
                            "81.8k",
                            "1.1k",
                            "7.0k",
                            "30.0k",
                            "26.7k",
                        ],
                    ),
                    (
                        "True Damage Dealt",
                        [
                            "25.5k",
                            "7.4k",
                            "3.3k",
                            "4.3k",
                            "2.6k",
                            "0.1k",
                            "17.9k",
                            "6.3k",
                            "4.1k",
                            "12.9k",
                        ],
                    ),
                    (
                        "Largest Critical Strike",
                        ["-", "-", "-", "600", "-", "-", "587", "-", "-", "-"],
                    ),
                    (
                        "Total Damage to Objectives",
                        [
                            "28.4k",
                            "3.7k",
                            "0.6k",
                            "4.9k",
                            "1.7k",
                            "6.9k",
                            "10.5k",
                            "1.8k",
                            "16.6k",
                            "21.3k",
                        ],
                    ),
                    (
                        "Total Damage to Turrets",
                        [
                            "0.7k",
                            "0.2k",
                            "0.0k",
                            "1.1k",
                            "0.6k",
                            "5.2k",
                            "9.2k",
                            "0.6k",
                            "10.0k",
                            "0.7k",
                        ],
                    ),
                    (
                        "Damage Healed",
                        [
                            "10.4k",
                            "1.9k",
                            "1.0k",
                            "2.4k",
                            "1.6k",
                            "5.8k",
                            "6.3k",
                            "2.6k",
                            "3.4k",
                            "11.1k",
                        ],
                    ),
                    (
                        "Damage Taken",
                        [
                            "31.6k",
                            "22.0k",
                            "19.5k",
                            "16.7k",
                            "16.0k",
                            "11.6k",
                            "21.4k",
                            "11.1k",
                            "10.7k",
                            "36.0k",
                        ],
                    ),
                    (
                        "Physical Damage Taken",
                        [
                            "22.6k",
                            "12.8k",
                            "10.7k",
                            "10.1k",
                            "6.8k",
                            "7.4k",
                            "17.3k",
                            "7.4k",
                            "7.4k",
                            "26.5k",
                        ],
                    ),
                    (
                        "Magic Damage Taken",
                        [
                            "7.1k",
                            "6.1k",
                            "7.5k",
                            "5.9k",
                            "8.2k",
                            "4.1k",
                            "2.7k",
                            "3.4k",
                            "2.2k",
                            "5.7k",
                        ],
                    ),
                    (
                        "True Damage Taken",
                        [
                            "1.9k",
                            "3.1k",
                            "1.3k",
                            "0.7k",
                            "1.1k",
                            "0.1k",
                            "1.3k",
                            "0.3k",
                            "1.1k",
                            "3.8k",
                        ],
                    ),
                    (
                        "Wards Placed",
                        ["4", "6", "12", "10", "9", "11", "8", "15", "6", "5"],
                    ),
                    (
                        "Wards Destroyed",
                        ["4", "3", "8", "-", "-", "3", "1", "8", "1", "3"],
                    ),
                    (
                        "Stealth Wards Purchased",
                        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
                    ),
                    (
                        "Control Wards Purchased",
                        ["1", "2", "1", "2", "2", "3", "1", "4", "-", "3"],
                    ),
                    (
                        "Gold Earned",
                        [
                            "11.0k",
                            "9.3k",
                            "5.8k",
                            "7.8k",
                            "7.4k",
                            "11.8k",
                            "11.7k",
                            "7.6k",
                            "14.4k",
                            "10.7k",
                        ],
                    ),
                    (
                        "Gold Spent",
                        [
                            "10.8k",
                            "9.0k",
                            "5.3k",
                            "7.3k",
                            "7.2k",
                            "10.8k",
                            "10.2k",
                            "5.5k",
                            "10.1k",
                            "10.3k",
                        ],
                    ),
                    (
                        "Minions Killed",
                        [
                            "37",
                            "168",
                            "29",
                            "162",
                            "150",
                            "176",
                            "160",
                            "32",
                            "211",
                            "20",
                        ],
                    ),
                    (
                        "Neutral Minions Killed",
                        ["136", "3", "-", "8", "-", "8", "12", "-", "4", "177"],
                    ),
                    (
                        "Neutral Minions Killed in Team's Jungle",
                        ["97", "-", "-", "3", "-", "4", "-", "-", "-", "96"],
                    ),
                    (
                        "Neutral Minions Killed in Enemy Jungle",
                        ["12", "1", "-", "-", "-", "4", "8", "-", "4", "33"],
                    ),
                ]
            ),
        )
