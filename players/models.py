from django.db import models

# Create your models here.


class Player(models.Model):
    username = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return f"{self.username}"
