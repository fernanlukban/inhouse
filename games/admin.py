from django.contrib import admin
from .models import EXPORTED_MODELS

# Register your models here.
for model in EXPORTED_MODELS:
    admin.site.register(model)