# Generated by Django 3.1.1 on 2020-09-20 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "username",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
        ),
    ]
