from bs4 import BeautifulSoup


class MatchHistory:
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.blue_side_bans, self.red_side_bans = MatchHistory.parse_bans(
            self.soup)
        self.blue_side_picks, self.red_side_picks = MatchHistory.parse_picks(
            self.soup)

    @classmethod
    def parse_bans(cls, soup):
        bans_container = soup.find_all('div', class_='bans-container')
        if len(bans_container) != 2:
            raise Exception("Could not properly find bans")
        return cls.find_champion_names_for_bans(
            bans_container[0]), cls.find_champion_names_for_bans(
            bans_container[1])

    @classmethod
    def find_champion_names_for_bans(cls, bans_container):
        champion_names = []
        for champion_nameplate_div in cls.parse_ban_container_for_champion_nameplate_div(
                bans_container):
            champion_name = champion_nameplate_div.find(
                lambda div: div.has_attr('data-rg-id'))['data-rg-id']
            champion_names.append(champion_name)
        return champion_names

    @classmethod
    def parse_ban_container_for_champion_nameplate_div(cls, bans_container):
        return bans_container.find_all('div', class_='champion-nameplate')

    @classmethod
    def parse_picks(cls, soup):
        # select lets us find a div that has both team and classic but in any order
        picks_container = soup.find_all('div', class_='team-selector')
        if len(picks_container) != 2:
            raise Exception("Could not properly find picks")
        return cls.find_champion_names_for_picks(picks_container[0]), cls.find_champion_names_for_picks(picks_container[1])

    @classmethod
    def find_champion_names_for_picks(cls, picks_container):
        champion_names = []
        for champion_name_div in picks_container.find_all(
                lambda div: div.has_attr('data-rg-id')):
            champion_names.append(champion_name_div['data-rg-id'])
        return champion_names

    @classmethod
    def from_file(cls, file_name):
        with open(file_name, 'r') as file:
            html = "".join(
                map(lambda line: line.rstrip('\n').rstrip('\r'), file))
            return cls(html)


class Bans:
    def __init__(self, bans_container_div):
        self._soup = bans_container_div