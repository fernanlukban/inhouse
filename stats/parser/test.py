from .html import MatchHistory
import unittest


class TestMatchHistory:
    def setUp(self):
        self.match = MatchHistory.from_file(
            '/mnt/c/Users/Fernan Lukban/Documents/inhouse/stats/parser/Match History Complete.html')
