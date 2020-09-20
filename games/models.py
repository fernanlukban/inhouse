from django.db import models
from django.apps import apps

SIDE_MAX_LENGTH = 10

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class GameInfo(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner = models.CharField(max_length=SIDE_MAX_LENGTH, null=True, blank=True)


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
