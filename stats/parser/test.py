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
