from django.db import models
from django.apps import apps
from players.models import Player

SIDE_MAX_LENGTH = 10

# Create your models here.
class CreateableFromMatchHistory:
    # Override this method to populate new model with information from match_history
    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        pass

    @classmethod
    def from_match_history(cls, match_history, *args, **kwargs):
        new_model = cls(*args, **kwargs)
        cls.setup_from_match_history(match_history, new_model)
        return new_model

    @classmethod
    def create_from_match_history(cls, match_history, *args, **kwargs):
        new_model = cls.from_match_history(cls, match_history, *args, **kwargs)
        new_model.save()
        return new_model


class SidedCreateableFromMatchHistory(CreateableFromMatchHistory):
    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        if "is_blue" not in kwargs:
            raise Exception("Need to pass in is_blue")
        CreateableFromMatchHistory.setup_from_match_history(
            cls, match_history, new_model, *args, **kwargs
        )

    @classmethod
    def setup_from_match_history_sided(
        cls, match_history, blue_new_model, red_new_model
    ):
        cls.setup_from_match_history(match_history, blue_new_model, is_blue=True)
        cls.setup_from_match_history(match_history, red_new_model, is_blue=False)

    @classmethod
    def from_match_history_sided(cls, match_history, *args, **kwargs):
        blue_new_model = cls(*args, **kwargs)
        red_new_model = cls(*args, **kwargs)
        cls.setup_from_match_history_sided(match_history, blue_new_model, red_new_model)
        return blue_new_model, red_new_model

    @classmethod
    def create_from_match_history_sided(cls, match_history, *args, **kwargs):
        blue_new_model, red_new_model = cls.create_from_match_history_sided(
            match_history, *args, **kwargs
        )
        blue_new_model.save()
        red_new_model.save()
        return blue_new_model, red_new_model


class Game(models.Model, CreateableFromMatchHistory):
    name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        pass

    def __str__(self):
        return f"Game {self.id}: {self.name if self.name else 'No name'}"


class GameInfo(models.Model, CreateableFromMatchHistory):
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    winner = models.CharField(max_length=SIDE_MAX_LENGTH, null=True, blank=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        new_model.winner = match_history.winner


class GameBanList(models.Model, SidedCreateableFromMatchHistory):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    ban_1 = models.CharField(max_length=20, default="None")
    ban_2 = models.CharField(max_length=20, default="None")
    ban_3 = models.CharField(max_length=20, default="None")
    ban_4 = models.CharField(max_length=20, default="None")
    ban_5 = models.CharField(max_length=20, default="None")
    blue_side = models.BooleanField(default=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue = kwargs["is_blue"]
        if is_blue:
            bans = match_history.blue_side_bans
            new_model.blue_side = True
        else:
            bans = match_history.red_side_bans
        for i, ban in enumerate(bans):
            setattr(new_model, f"ban_{i}", ban)

    def __str__(self):
        return f"GameBanList(info={self.info.game}, [{', '.join([getattr(self, f'ban_{i}') for i in range(1,6)])}]"


class GamePickList(models.Model, SidedCreateableFromMatchHistory):
    info = models.ForeignKey(GameInfo, on_delete=models.CASCADE)
    pick_1 = models.CharField(max_length=20)
    pick_2 = models.CharField(max_length=20)
    pick_3 = models.CharField(max_length=20)
    pick_4 = models.CharField(max_length=20)
    pick_5 = models.CharField(max_length=20)
    blue_side = models.BooleanField(default=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue = kwargs["is_blue"]
        if is_blue:
            picks = match_history.blue_side_picks
            new_model.blue_side = True
        else:
            bans = match_history.red_side_picks
        for i, pick in enumerate(picks):
            setattr(new_model, f"ban_{i}", pick)


class GamePlayer(models.Model, CreateableFromMatchHistory):
    player = models.OneToOneField(
        "players.Player", on_delete=models.CASCADE, null=True, blank=True
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    blue_side = models.BooleanField(default=True)
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
                new_game_player.blue_side = True if i == 0 else False
                if "player" in kwargs:
                    new_game_player.player = kwargs["player"]
                else:
                    try:
                        player_object_from_player_name = Player.objects.get()
                    except Player.DoesNotExist:
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
        return f"Game: {self.game}/Player: {self.player}/Side: {'blue' if self.blue_side else 'red'}"


EXPORTED_MODELS = [Game, GameInfo, GameBanList, GamePickList, GamePlayer]
