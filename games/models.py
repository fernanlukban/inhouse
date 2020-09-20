from django.db import models
from django.apps import apps

SIDE_MAX_LENGTH = 10

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def from_match_history(cls, match_history, *args, **kwargs):
        new_game = cls(*args, **kwargs)
        return new_game

    @classmethod
    def create_from_match_history(cls, match_history, *args, **kwargs):
        new_game = cls.from_match_history(cls, match_history, *args, **kwargs)
        new_game.save()
        return new_game

    def __str__(self):
        return f"Game {self.id}: {self.name if self.name else 'No name'}"


class GameInfo(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner = models.CharField(max_length=SIDE_MAX_LENGTH, null=True, blank=True)

    @classmethod
    def from_match_history(cls, match_history, *args, **kwargs):
        new_game_info = cls(*args, **kwargs)
        new_game_info.winner = match_history.winner
        return new_game_info

    @classmethod
    def create_from_match_history(cls, match_history, *args, **kwargs):
        new_game_info = cls.new_game_info(match_history, *args, **kwargs)
        new_game_info.save()
        return new_game_info


class GameBanList(models.Model):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    ban_1 = models.CharField(max_length=20)
    ban_2 = models.CharField(max_length=20)
    ban_3 = models.CharField(max_length=20)
    ban_4 = models.CharField(max_length=20)
    ban_5 = models.CharField(max_length=20)
    blue_side = models.BooleanField(default=True)


class GamePickList(models.Model):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    pick_1 = models.CharField(max_length=20)
    pick_2 = models.CharField(max_length=20)
    pick_3 = models.CharField(max_length=20)
    pick_4 = models.CharField(max_length=20)
    pick_5 = models.CharField(max_length=20)
    blue_side = models.BooleanField(default=True)


class GamePlayer(models.Model):
    player = models.OneToOneField("players.Player", on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    blue_side = models.BooleanField(default=True)
    champion = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, null=True, blank=True)
    captain = models.BooleanField(default=False)
    pick_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Game: {self.game}/Player: {self.player}/Side: {'blue' if self.blue_side else 'red'}"


EXPORTED_MODELS = [Game, GameInfo, GameBanList, GamePickList, GamePlayer]
