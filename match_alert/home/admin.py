from django.contrib import admin
from home import models as home

admin.site.register(home.League)
admin.site.register(home.Team)
admin.site.register(home.LeagueTable)
admin.site.register(home.Fixture)
admin.site.register(home.Result)
