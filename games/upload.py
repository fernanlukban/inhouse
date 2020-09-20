from games.models import *
from stats.models import *


def handle_uploaded_match_history(name, description, file):
    print(f"New game uploaded: {name} - {description}")
    file.open()
    print()