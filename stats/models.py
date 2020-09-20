from django.db import models
from .parser.utils import SidedCreateableFromMatchHistory

# Create your models here.
class GameStat(models.Model):
    game = models.OneToOneField("games.Game", on_delete=models.CASCADE)

    def __str__(self):
        game_name = self.game.name
        return f"{game_name}"


class GameCombatStat(models.Model, SidedCreateableFromMatchHistory):
    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
    FIRST_BLOOD_CHOICES = [
        (0, "Not on this team"),
        (1, "Player 1"),
        (2, "Player 2"),
        (3, "Player 3"),
        (4, "Player 4"),
        (5, "Player 5"),
    ]
    kills_1 = models.IntegerField(default=0)
    kills_2 = models.IntegerField(default=0)
    kills_3 = models.IntegerField(default=0)
    kills_4 = models.IntegerField(default=0)
    kills_5 = models.IntegerField(default=0)
    deaths_1 = models.IntegerField(default=0)
    deaths_2 = models.IntegerField(default=0)
    deaths_3 = models.IntegerField(default=0)
    deaths_4 = models.IntegerField(default=0)
    deaths_5 = models.IntegerField(default=0)
    assists_1 = models.IntegerField(default=0)
    assists_2 = models.IntegerField(default=0)
    assists_3 = models.IntegerField(default=0)
    assists_4 = models.IntegerField(default=0)
    assists_5 = models.IntegerField(default=0)
    largest_killing_spree_1 = models.IntegerField(default=0)
    largest_killing_spree_2 = models.IntegerField(default=0)
    largest_killing_spree_3 = models.IntegerField(default=0)
    largest_killing_spree_4 = models.IntegerField(default=0)
    largest_killing_spree_5 = models.IntegerField(default=0)
    largest_multi_kill_1 = models.IntegerField(default=0)
    largest_multi_kill_2 = models.IntegerField(default=0)
    largest_multi_kill_3 = models.IntegerField(default=0)
    largest_multi_kill_4 = models.IntegerField(default=0)
    largest_multi_kill_5 = models.IntegerField(default=0)
    first_blood = models.IntegerField(default=0, choices=FIRST_BLOOD_CHOICES)
    is_blue_side = models.BooleanField(default=True)

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue = kwargs["is_blue"]
        if is_blue:
            pass
        else:
            new_model.is_blue_side = False


class GameDamageStat(models.Model, SidedCreateableFromMatchHistory):
    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
    total_damage_to_champs_1 = models.IntegerField(default=0)
    total_damage_to_champs_2 = models.IntegerField(default=0)
    total_damage_to_champs_3 = models.IntegerField(default=0)
    total_damage_to_champs_4 = models.IntegerField(default=0)
    total_damage_to_champs_5 = models.IntegerField(default=0)


class GameWardStat(models.Model, SidedCreateableFromMatchHistory):
    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
    wards_placed_1 = models.IntegerField(default=0)
    wards_placed_2 = models.IntegerField(default=0)
    wards_placed_3 = models.IntegerField(default=0)
    wards_placed_4 = models.IntegerField(default=0)
    wards_placed_5 = models.IntegerField(default=0)
    wards_destroyed_1 = models.IntegerField(default=0)
    wards_destroyed_2 = models.IntegerField(default=0)
    wards_destroyed_3 = models.IntegerField(default=0)
    wards_destroyed_4 = models.IntegerField(default=0)
    wards_destroyed_5 = models.IntegerField(default=0)
    control_wards_purchased_1 = models.IntegerField(default=0)
    control_wards_purchased_2 = models.IntegerField(default=0)
    control_wards_purchased_3 = models.IntegerField(default=0)
    control_wards_purchased_4 = models.IntegerField(default=0)
    control_wards_purchased_5 = models.IntegerField(default=0)


class GameIncomeStat(models.Model, SidedCreateableFromMatchHistory):
    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
    gold_earned_1 = models.IntegerField(default=0)
    gold_earned_2 = models.IntegerField(default=0)
    gold_earned_3 = models.IntegerField(default=0)
    gold_earned_4 = models.IntegerField(default=0)
    gold_earned_5 = models.IntegerField(default=0)
    gold_spent_1 = models.IntegerField(default=0)
    gold_spent_2 = models.IntegerField(default=0)
    gold_spent_3 = models.IntegerField(default=0)
    gold_spent_4 = models.IntegerField(default=0)
    gold_spent_5 = models.IntegerField(default=0)
    minions_killed_1 = models.IntegerField(default=0)
    minions_killed_2 = models.IntegerField(default=0)
    minions_killed_3 = models.IntegerField(default=0)
    minions_killed_4 = models.IntegerField(default=0)
    minions_killed_5 = models.IntegerField(default=0)
    neutral_minions_killed_1 = models.IntegerField(default=0)
    neutral_minions_killed_2 = models.IntegerField(default=0)
    neutral_minions_killed_3 = models.IntegerField(default=0)
    neutral_minions_killed_4 = models.IntegerField(default=0)
    neutral_minions_killed_5 = models.IntegerField(default=0)


class PlayerStat(models.Model):
    player = models.OneToOneField("players.Player", on_delete=models.CASCADE)
