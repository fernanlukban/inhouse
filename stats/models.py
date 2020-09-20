from django.db import models
from .parser.utils import SidedCreateableFromMatchHistory


class SidedCreatableStatsFromMatchHistory(SidedCreateableFromMatchHistory):
    @staticmethod
    def format_with_k_to_int(text):
        # turns 1k to 1000
        return int(float(text[:-1]) * 1000)

    @staticmethod
    def format_with_null(text):
        return 0 if "-" in text else int(text)

    @classmethod
    def setup_stats(
        cls, match_history, new_model, is_blue_side, header, field_name, fmt
    ):
        if is_blue_side:
            header_values = match_history.stats[header][:5]
        else:
            header_values = match_history.stats[header][5:]
        for i, header_text in enumerate(header_values):
            new_value = fmt(header_text)
            setattr(new_model, f"{field_name}_{i+1}", new_value)


# Create your models here.
class GameStat(models.Model):
    game = models.OneToOneField("games.Game", on_delete=models.CASCADE)

    def __str__(self):
        return f"GameStat(game={self.game})"


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
        return [getattr(self, f"largest_multi_kill_{i+1}") for i in range(5)]

    def __str__(self):
        return f"GameCombatStat({'blue' if self.is_blue_side else 'red'}, {self.kills}, {self.deaths}, {self.assists}, {self.largest_killing_sprees}, {self.largest_multi_kills})"

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
            cls.LARGEST_KILLING_SPREE,
            cls.CONVERT[cls.LARGEST_KILLING_SPREE],
            int,
        )
        cls.setup_stats(
            match_history,
            new_model,
            is_blue_side,
            cls.LARGEST_MULTI_KILL,
            cls.CONVERT[cls.LARGEST_MULTI_KILL],
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
            kills, deaths, assists = map(lambda x: int(x), kda.split("/"))
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
    is_blue_side = models.BooleanField(default=True)

    @property
    def total_damage_to_champs(self):
        return [
            getattr(
                self,
                f"{GameDamageStat.CONVERT[GameDamageStat.TOTAL_DAMAGE_TO_CHAMPIONS]}_{i+1}",
            )
            for i in range(5)
        ]

    def __str__(self):
        return f"GameDamageStat({'blue' if self.is_blue_side else 'red'}, {self.total_damage_to_champs})"

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
            cls.TOTAL_DAMAGE_TO_CHAMPIONS,
            cls.CONVERT[cls.TOTAL_DAMAGE_TO_CHAMPIONS],
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
    is_blue_side = models.BooleanField(default=True)

    @property
    def wards_placed(self):
        return [
            getattr(self, f"{GameWardStat.CONVERT[GameWardStat.WARDS_PLACED]}_{i+1}")
            for i in range(5)
        ]

    @property
    def wards_destroyed(self):
        return [
            getattr(self, f"{GameWardStat.CONVERT[GameWardStat.WARDS_DESTROYED]}_{i+1}")
            for i in range(5)
        ]

    @property
    def control_wards_purchased(self):
        return [
            getattr(
                self,
                f"{GameWardStat.CONVERT[GameWardStat.CONTROL_WARDS_PURCHASED]}_{i+1}",
            )
            for i in range(5)
        ]

    def __str__(self):
        return f"GameWardStat({'blue' if self.is_blue_side else 'red'}, {self.wards_placed}, {self.wards_destroyed}, {self.control_wards_purchased})"

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
        for header, field in cls.CONVERT.items():
            cls.setup_stats(
                match_history,
                new_model,
                is_blue_side,
                header,
                field,
                SidedCreatableStatsFromMatchHistory.format_with_null,
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
    is_blue_side = models.BooleanField(default=True)

    @property
    def gold_earned(self):
        return [
            getattr(
                self, f"{GameIncomeStat.CONVERT[GameIncomeStat.GOLD_EARNED][0]}_{i+1}"
            )
            for i in range(5)
        ]

    @property
    def gold_spent(self):
        return [
            getattr(
                self, f"{GameIncomeStat.CONVERT[GameIncomeStat.GOLD_SPENT][0]}_{i+1}"
            )
            for i in range(5)
        ]

    @property
    def minions_killed(self):
        return [
            getattr(
                self,
                f"{GameIncomeStat.CONVERT[GameIncomeStat.MINIONS_KILLED][0]}_{i+1}",
            )
            for i in range(5)
        ]

    @property
    def neutral_minions_killed(self):
        return [
            getattr(
                self,
                f"{GameIncomeStat.CONVERT[GameIncomeStat.NEUTRAL_MINIONS_KILLED][0]}_{i+1}",
            )
            for i in range(5)
        ]

    def __str__(self):
        return f"GameIncomeStat({'blue' if self.is_blue_side else 'red'}, {self.gold_earned}, {self.gold_spent}, {self.minions_killed}, {self.neutral_minions_killed})"

    GOLD_EARNED = "Gold Earned"
    GOLD_SPENT = "Gold Spent"
    MINIONS_KILLED = "Minions Killed"
    NEUTRAL_MINIONS_KILLED = "Neutral Minions Killed"

    CONVERT = {
        GOLD_EARNED: (
            "gold_earned",
            SidedCreatableStatsFromMatchHistory.format_with_k_to_int,
        ),
        GOLD_SPENT: (
            "gold_spent",
            SidedCreatableStatsFromMatchHistory.format_with_k_to_int,
        ),
        MINIONS_KILLED: (
            "minions_killed",
            SidedCreatableStatsFromMatchHistory.format_with_null,
        ),
        NEUTRAL_MINIONS_KILLED: (
            "neutral_minions_killed",
            SidedCreatableStatsFromMatchHistory.format_with_null,
        ),
    }

    @classmethod
    def setup_from_match_history(cls, match_history, new_model, *args, **kwargs):
        is_blue_side = kwargs["is_blue_side"]
        if not is_blue_side:
            new_model.is_blue_side = False
        for header, (field, formatter) in cls.CONVERT.items():
            cls.setup_stats(
                match_history,
                new_model,
                is_blue_side,
                header,
                field,
                formatter,
            )


class PlayerStat(models.Model):
    player = models.OneToOneField("players.Player", on_delete=models.CASCADE)
