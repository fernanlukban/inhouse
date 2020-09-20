from django.contrib import admin
from .models import (
    GameStat,
    GameCombatStat,
    GameDamageStat,
    GameWardStat,
    GameIncomeStat,
)

# Register your models here.
admin.site.register(GameStat)
admin.site.register(GameCombatStat)
admin.site.register(GameDamageStat)
admin.site.register(GameWardStat)
admin.site.register(GameIncomeStat)
