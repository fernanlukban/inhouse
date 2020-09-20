from .html import MatchHistory
import unittest


class TestMatchHistory(unittest.TestCase):
    def setUp(self):
        self.match = MatchHistory.from_file(
            '/mnt/c/Users/Fernan Lukban/Documents/inhouse/stats/parser/Match History Complete.html')

    def test_parse_bans(self):
        self.assertEqual(self.match.blue_side_bans, [
                         'Akali', 'Blitzcrank', 'Annie', 'Ashe', 'Senna'])
        self.assertEqual(self.match.red_side_bans, [
            'Evelynn', 'Karthus', 'Talon', 'Nidalee', 'Kayle'])

    def test_parse_picks(self):
        self.assertEqual(self.match.blue_side_picks, [
                         'MasterYi', 'Riven', 'Thresh', 'Caitlyn', 'Syndra'])
        self.assertEqual(self.match.red_side_picks, [
                         'Lulu', 'Fiora', 'Rakan', 'Ezreal', 'Hecarim'])

    def test_parse_players(self):
        self.assertEqual(self.match.blue_side_players, [
                         'FruitSmoothie27', 'Shinigámí', 'Koó', 'enwards', 'Vassallo'])
        self.assertEqual(self.match.red_side_players, [
                         'fk the system', 'Chicago Boy', 'Espia', 'KeIlen', 'opsadboys'])

    def test_parse_objectives(self):
        self.assertEqual(self.blue_side_objectives, {
                         'tower_kills': '1', 'baron_kills': '0', 'dragon_kills': '0', 'rift_herald_kills': '2', 'inhibitor_kills': '0'})
        self.assertEqual(self.red_side_objectives, {
                         'tower_kills': '9', 'baron_kills': '0', 'dragon_kills': '4', 'rift_herald_kills': '0', 'inhibitor_kills': '1'})
