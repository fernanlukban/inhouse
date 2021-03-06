from bs4 import BeautifulSoup
from collections import OrderedDict


class MatchHistory:
    OBJECTIVES = {
        "tower_kills": "tower-kills",
        "baron_kills": "baron-kills",
        "dragon_kills": "dragon-kills",
        "rift_herald_kills": "rift-herald-kills",
        "inhibitor_kills": "inhibitor-kills",
    }

    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.blue_side_bans, self.red_side_bans = MatchHistory.parse_bans(self.soup)
        self.blue_side_picks, self.red_side_picks = MatchHistory.parse_picks(self.soup)
        self.blue_side_players, self.red_side_players = MatchHistory.parse_players(
            self.soup
        )
        (
            self.blue_side_objectives,
            self.red_side_objectives,
        ) = MatchHistory.parse_objectives(self.soup)
        self.stats = MatchHistory.parse_stats(self.soup)
        self.winner = MatchHistory.parse_winner(self.soup)

    @classmethod
    def parse_bans(cls, soup):
        bans_container = soup.find_all("div", class_="bans-container")
        if len(bans_container) != 2:
            raise Exception("Could not properly find bans")
        return (
            cls.find_champion_names_for_bans(bans_container[0]),
            cls.find_champion_names_for_bans(bans_container[1]),
        )

    @classmethod
    def find_champion_names_for_bans(cls, bans_container):
        champion_names = []
        for champion_nameplate_div in bans_container.find_all(
            "div", class_="champion-nameplate"
        ):
            champion_name = champion_nameplate_div.find(
                lambda div: div.has_attr("data-rg-id")
            )["data-rg-id"]
            champion_names.append(champion_name)
        return champion_names

    @classmethod
    def parse_picks(cls, soup):
        # select lets us find a div that has both team and classic but in any order
        picks_container = soup.find_all("div", class_="team-selector")
        if len(picks_container) < 2:
            picks_container = soup.find_all("div", class_="champion-icon binding")[:10]
            champion_names = []
            for pick in picks_container:
                champion_name = pick.find(lambda div: div.has_attr("data-rg-id"))
                champion_names.append(champion_name["data-rg-id"])
            return champion_names[:5], champion_names[5:]
        else:
            blue_picks = picks_container[0]
            red_picks = picks_container[1]
        return (
            cls.find_champion_names_for_picks(blue_picks),
            cls.find_champion_names_for_picks(red_picks),
        )

    @classmethod
    def find_champion_names_for_picks(cls, picks_container):
        champion_names = []
        for champion_name_div in picks_container.find_all(
            lambda div: div.has_attr("data-rg-id")
        ):
            champion_names.append(champion_name_div["data-rg-id"])
        return champion_names

    @classmethod
    def parse_players(cls, soup):
        players = []
        for player_div in soup.find_all("div", class_="champion-nameplate-name"):
            player_link = player_div.find("a")
            players.append(player_link.text)
        return players[:5], players[5:]

    @classmethod
    def parse_objectives(cls, soup):
        objectives = [{}, {}]
        for i in range(len(objectives)):
            for objective, div_class in cls.OBJECTIVES.items():
                objective_divs = soup.find_all("div", class_=div_class)
                objectives[i][objective] = objective_divs[i].find("span").text
        return objectives

    @classmethod
    def parse_stats(cls, soup):
        table = soup.find(id="stats")
        stats = OrderedDict()
        for row in table.find_all("tr"):
            row_name = row.find("div", class_="view")
            if row_name is None:
                continue
            row_stats = []
            cells = row.find_all("div", class_="grid-cell")
            if cells is None:
                continue
            for column in cells:
                row_stats.append(column.text)
            if row_name.text != "":
                stats[row_name.text] = row_stats
        return stats

    @classmethod
    def parse_winner(cls, soup):
        summary = soup.find("div", class_="team-summary")
        blue_win = summary.find("div", class_="game-conclusion").text.strip()
        return "blue" if blue_win == "VICTORY" else "red"

    @classmethod
    def from_file(cls, file_name):
        with open(file_name, "r") as file:
            return cls(file)


class Bans:
    def __init__(self, bans_container_div):
        self._soup = bans_container_div
