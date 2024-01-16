"""
URL configuration for match_alert project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.HomeView.as_view(), name="home"),
    path(
        "table/<slug:slug>/", home_views.LeagueTableView.as_view(), name="league_table"
    ),
    path("<slug:slug>/", home_views.LeagueTeamsView.as_view(), name="league_teams"),
    path(
        "fixtures/<slug:slug>/",
        home_views.LeagueFixturesView.as_view(),
        name="league_fixtures",
    ),
    path(
        "results/<slug:slug>/",
        home_views.LeagueResultsView.as_view(),
        name="league_results",
    ),
    path("auth/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
