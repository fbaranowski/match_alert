from django.contrib import admin
from home import models as home


class LeagueAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"team_slug": ("name",)}


admin.site.register(home.League, LeagueAdmin)
admin.site.register(home.Team, TeamAdmin)
admin.site.register(home.LeagueTable)
admin.site.register(home.Fixture)
admin.site.register(home.Result)
