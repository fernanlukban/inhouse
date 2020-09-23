from django import forms
from players.models import Player


class DuoForm(forms.Form):
    username1 = forms.ModelChoiceField(queryset=Player.objects.all())
    username2 = forms.ModelChoiceField(queryset=Player.objects.all())
