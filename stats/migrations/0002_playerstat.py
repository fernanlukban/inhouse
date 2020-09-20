# Generated by Django 3.1.1 on 2020-09-20 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("players", "0001_initial"),
        ("stats", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerStat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "player",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="players.player"
                    ),
                ),
            ],
        ),
    ]
