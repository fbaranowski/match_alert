from django.contrib import admin
import dashboard.models as dashboard

admin.site.register(dashboard.Team)
admin.site.register(dashboard.Table)
admin.site.register(dashboard.Result)
admin.site.register(dashboard.Fixture)
