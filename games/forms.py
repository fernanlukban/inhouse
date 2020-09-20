from django import forms


class MatchHistoryFileFieldForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=200)
    match_history_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )
