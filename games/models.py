from django.db import models
from django.apps import apps
from players.models import Player
from stats.parser.utils import (
    CreateableFromMatchHistory,
    SidedCreateableFromMatchHistory,
)

SIDE_MAX_LENGTH = 10

# Create your models here.
class Game(models.Model, CreateableFromMatchHistory):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        pass

    def __str__(self):
        return f"Game {self.id}: Title - {self.name if self.name else 'No name'}/Description - {self.description}"


class GameInfo(models.Model, CreateableFromMatchHistory):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner = models.CharField(max_length=SIDE_MAX_LENGTH, null=True, blank=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        new_model.winner = match_history.winner

    def __str__(self):
        return f"GameInfo(winner: {self.winner})"


class GameBanList(models.Model, SidedCreateableFromMatchHistory):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    ban_1 = models.CharField(max_length=20, default="None")
    ban_2 = models.CharField(max_length=20, default="None")
    ban_3 = models.CharField(max_length=20, default="None")
    ban_4 = models.CharField(max_length=20, default="None")
    ban_5 = models.CharField(max_length=20, default="None")
    is_blue_side = models.BooleanField(default=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if is_blue_side:
            bans = match_history.blue_side_bans
        else:
            bans = match_history.red_side_bans
            new_model.is_blue_side = False
        for i, ban in enumerate(bans):
            setattr(new_model, f"ban_{i+1}", ban)

    def __str__(self):
        return f"GameBanList(info={self.info.game}, {self.bans})"

    @property
    def bans(self):
        return [getattr(self, f"ban_{i+1}") for i in range(5)]


class GamePickList(models.Model, SidedCreateableFromMatchHistory):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    pick_1 = models.CharField(max_length=20)
    pick_2 = models.CharField(max_length=20)
    pick_3 = models.CharField(max_length=20)
    pick_4 = models.CharField(max_length=20)
    pick_5 = models.CharField(max_length=20)
    is_blue_side = models.BooleanField(default=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if is_blue_side:
            picks = match_history.blue_side_picks
        else:
            picks = match_history.red_side_picks
            new_model.is_blue_side = False
        for i, pick in enumerate(picks):
            setattr(new_model, f"pick_{i+1}", pick)

    def __str__(self):
        return f"GamePickList(info={self.info.game}, {self.picks})"

    @property
    def picks(self):
        return [getattr(self, f"pick_{i+1}") for i in range(5)]


class GamePlayer(models.Model, CreateableFromMatchHistory):
    player = models.ForeignKey(
        "players.Player", on_delete=models.CASCADE, null=True, blank=True
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    is_blue_side = models.BooleanField(default=True)
    champion = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, null=True, blank=True)
    captain = models.BooleanField(default=False)
    pick_order = models.IntegerField(null=True, blank=True)

    @classmethod
    def from_match_history_all(cls, match_history, *args, **kwargs):
        if "game" not in kwargs:
            raise Exception("Need to pass in game")
        players = []
        player_names_and_picks_zipped = (
            zip(match_history.blue_side_players, match_history.blue_side_picks),
            zip(match_history.red_side_players, match_history.red_side_picks),
        )
        for i, players_on_one_side in enumerate(player_names_and_picks_zipped):
            for j, (player_name, champion) in enumerate(players_on_one_side):
                new_game_player = GamePlayer()
                new_game_player.game = kwargs["game"]
                new_game_player.champion = champion
                new_game_player.is_blue_side = True if i == 0 else False
                try:
                    print("getting already created player")
                    player_object_from_player_name = Player.objects.get(
                        username=player_name
                    )
                except Player.DoesNotExist:
                    print("creating new player")
                    player_object_from_player_name = Player.objects.create(
                        username=player_name
                    )
                new_game_player.player = player_object_from_player_name
                players.append(new_game_player)
        return players

    @classmethod
    def create_from_match_history_all(cls, match_history, *args, **kwargs):
        players = cls.from_match_history_all(cls, match_history, *args, **kwargs)
        for player in players:
            player.save()
        return players

    @classmethod
    def create_from_match_history_all(cls, match_history, *args, **kwargs):
        return super().create_from_match_history(match_history, *args, **kwargs)

    def __str__(self):
        return f"Game: {self.game}/Player: {self.player}/Side: {'blue' if self.is_blue_side else 'red'}"


EXPORTED_MODELS = [Game, GameInfo, GameBanList, GamePickList, GamePlayer]
