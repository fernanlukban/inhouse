from django.db import models

# Create your models here.


class GameStat(models.Model):
    game = models.OneToOneField("games.Game", on_delete=models.CASCADE)

    def __str__(self):
        game_name = self.game.name
        return f"{game_name}"

    @classmethod
    def from_match_history(cls, match_history):
        return cls()


class PlayerStat(models.Model):
    player = models.OneToOneField("players.Player", on_delete=models.CASCADE)
