from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_date', 'rating')

admin.site.register(Game, GameAdmin)


# Register your models here.
