from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse
from .forms import MatchHistoryFileFieldForm
from .upload import handle_uploaded_match_history
from .models import Game

# Create your views here.
def upload_match_history(request):
    if request.method == "POST":
        form = MatchHistoryFileFieldForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_match_history(
                form.data["name"],
                form.data["description"],
                request.FILES["match_history_file"],
            )
            return HttpResponseRedirect(reverse("games:show_games"))
        else:
            print("not valid")
    else:
        form = MatchHistoryFileFieldForm()
    return render(request, "games/upload.html", {"form": form})


def show_games(request):
    games = Game.objects.all()
    return render(request, "games/index.html", {"games": games})