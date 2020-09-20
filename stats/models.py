from django.db import models
from .parser.utils import SidedCreateableFromMatchHistory


class SidedCreatableStatsFromMatchHistory(SidedCreateableFromMatchHistory):
    @staticmethod
    def format_with_k_to_int(text):
        # turns 1k to 1000
        return int(float(text[:-1]) * 1000)

    @classmethod
    def setup_stats(
        cls, match_history, new_model, is_blue_side, header, field_name, fmt
    ):
        if is_blue_side:
            header_values = match_history.stats[header][:5]
        else:
            header_values = match_history.stats[header][5:]
        for i, header_text in enumerate(header_values):
            largest_killing_spree = fmt(header_text)
            setattr(
                new_model,
                f"{field_name}_{i+1}",
            )


# Create your models here.
class GameStat(models.Model):
    game = models.OneToOneField("games.Game", on_delete=models.CASCADE)

    def __str__(self):
        game_name = self.game.name
        return f"{game_name}"


class GameCombatStat(models.Model, SidedCreatableStatsFromMatchHistory):
    FIRST_BLOOD_CHOICES = [
        (0, "Not on this team"),
        (1, "Player 1"),
        (2, "Player 2"),
        (3, "Player 3"),
        (4, "Player 4"),
        (5, "Player 5"),
    ]

    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
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

    @property
    def kills(self):
        return [getattr(self, f"kills_{i+1}") for i in range(5)]

    @property
    def deaths(self):
        return [getattr(self, f"deaths_{i+1}") for i in range(5)]

    @property
    def assists(self):
        return [getattr(self, f"assists_{i+1}") for i in range(5)]

    @property
    def largest_killing_sprees(self):
        return [getattr(self, f"largest_killing_spree_{i+1}") for i in range(5)]

    @property
    def largest_multi_kills(self):
        return [getattr(self, f"largest_multi_kill_5_{i+1}") for i in range(5)]

    KDA = "KDA"
    LARGEST_KILLING_SPREE = "Largest Killing Spree"
    LARGEST_MULTI_KILL = "Largest Multi Kill"
    FIRST_BLOOD = "First Blood"

    FIRST_BLOOD_INDICATOR = "●"

    CONVERT = {
        LARGEST_KILLING_SPREE: "largest_killing_spree",
        LARGEST_MULTI_KILL: "largest_multi_kill",
        FIRST_BLOOD: "first_blood",
    }

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if not is_blue_side:
            new_model.is_blue_side = False
        cls.setup_kda(match_history, new_model, is_blue_side)
        cls.setup_stats(
            match_history,
            new_model,
            is_blue_side,
            LARGEST_KILLING_SPREE,
            CONVERT[LARGEST_KILLING_SPREE],
            int,
        )
        cls.setup_stats(
            match_history,
            new_model,
            is_blue_side,
            LARGEST_MULTI_KILL,
            CONVERT[LARGEST_MULTI_KILL],
            int,
        )
        cls.setup_first_blood(match_history, new_model, is_blue_side)

    @classmethod
    def setup_kda(cls, match_history, new_model, is_blue_side):
        if is_blue_side:
            kdas = match_history.stats[GameCombatStat.KDA][:5]
        else:
            kdas = match_history.stats[GameCombatStat.KDA][5:]
        for i, kda in enumerate(kdas):
            kills, deaths, assists = map(kdas.split("/"), lambda x: int(x))
            setattr(new_model, f"kills_{i+1}", kills)
            setattr(new_model, f"deaths_{i+1}", deaths)
            setattr(new_model, f"assists_{i+1}", assists)

    @classmethod
    def setup_first_blood(cls, match_history, new_model, is_blue_side):
        if is_blue_side:
            first_bloods = match_history.stats[GameCombatStat.FIRST_BLOOD][:5]
        else:
            first_bloods = match_history.stats[GameCombatStat.FIRST_BLOOD][5:]
        # iterate over until we find the indicator, and use that
        # if it's not there it's just 0
        for i, indicator in enumerate(first_bloods):
            if indicator == GameCombatStat.FIRST_BLOOD_INDICATOR:
                new_model.first_blood = i + 1
                return
        new_model.first_blood = 0


class GameDamageStat(models.Model, SidedCreatableStatsFromMatchHistory):
    game_stat = models.ForeignKey(GameStat, on_delete=models.CASCADE)
    total_damage_to_champs_1 = models.IntegerField(default=0)
    total_damage_to_champs_2 = models.IntegerField(default=0)
    total_damage_to_champs_3 = models.IntegerField(default=0)
    total_damage_to_champs_4 = models.IntegerField(default=0)
    total_damage_to_champs_5 = models.IntegerField(default=0)

    @property
    def total_damage_to_champs(self):
        return [
            getattr(self, f"{CONVERT[TOTAL_DAMAGE_TO_CHAMPIONS]}_{i+1}")
            for i in range(5)
        ]

    TOTAL_DAMAGE_TO_CHAMPIONS = "Total Damage to Champions"

    CONVERT = {TOTAL_DAMAGE_TO_CHAMPIONS: "total_damage_to_champs"}

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if not is_blue_side:
            new_model.is_blue_side = False
        cls.setup_stats(
            match_history,
            new_model,
            is_blue_side,
            TOTAL_DAMAGE_TO_CHAMPIONS,
            CONVERT[TOTAL_DAMAGE_TO_CHAMPIONS],
            SidedCreatableStatsFromMatchHistory.format_with_k_to_int,
        )


class GameWardStat(models.Model, SidedCreatableStatsFromMatchHistory):
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

    @property
    def wards_placed(self):
        return [getattr(self, f"{CONVERT[WARDS_PLACED]}_{i+1}") for i in range(5)]

    @property
    def wards_destroyed(self):
        return [getattr(self, f"{CONVERT[WARDS_DESTROYED]}_{i+1}") for i in range(5)]

    @property
    def control_wards_purchased(self):
        return [
            getattr(self, f"{CONVERT[CONTROL_WARDS_PURCHASED]}_{i+1}") for i in range(5)
        ]

    WARDS_PLACED = "Wards Placed"
    WARDS_DESTROYED = "Wards Destroyed"
    CONTROL_WARDS_PURCHASED = "Control Wards Purchased"

    CONVERT = {
        WARDS_PLACED: "wards_placed",
        WARDS_DESTROYED: "wards_destroyed",
        CONTROL_WARDS_PURCHASED: "control_wards_purchased",
    }

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if not is_blue_side:
            new_model.is_blue_side = False
        for header, field in CONVERT.items():
            cls.setup_stats(
                match_history,
                new_model,
                is_blue_side,
                header,
                field,
                SidedCreatableStatsFromMatchHistory.format_with_k_to_int,
            )


class GameIncomeStat(models.Model, SidedCreatableStatsFromMatchHistory):
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

    @property
    def gold_earned(self):
        return [getattr(self, f"{CONVERT[GOLD_EARNED]}_{i+1}") for i in range(5)]

    @property
    def gold_spent(self):
        return [getattr(self, f"{CONVERT[GOLD_SPENT]}_{i+1}") for i in range(5)]

    @property
    def minions_killed(self):
        return [getattr(self, f"{CONVERT[MINIONS_KILLED]}_{i+1}") for i in range(5)]

    @property
    def neutral_minions_killed(self):
        return [
            getattr(self, f"{CONVERT[NEUTRAL_MINIONS_KILLED]}_{i+1}") for i in range(5)
        ]

    GOLD_EARNED = "Gold Earned"
    GOLD_SPENT = "Gold Spent"
    MINIONS_KILLED = "Minions Killed"
    NEUTRAL_MINIONS_KILLED = "Neutral Minions Killed"

    CONVERT = {
        GOLD_EARNED: "gold_earned",
        GOLD_SPENT: "gold_spent",
        MINIONS_KILLED: "minions_killed",
        NEUTRAL_MINIONS_KILLED: "neutral_minions_killed",
    }

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if not is_blue_side:
            new_model.is_blue_side = False
        for header, field in CONVERT.items():
            cls.setup_stats(
                match_history,
                new_model,
                is_blue_side,
                header,
                field,
                SidedCreatableStatsFromMatchHistory.format_with_k_to_int,
            )


class PlayerStat(models.Model):
    player = models.OneToOneField("players.Player", on_delete=models.CASCADE)
