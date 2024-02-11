from django.urls import path
from users import views as user_views

urlpatterns = [
    path("register/", user_views.RegisterView.as_view(), name="register"),
    path("login/", user_views.CustomLoginView.as_view(), name="login"),
    path("logout/", user_views.CustomLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", user_views.ProfileView.as_view(), name="profile"),
    path(
        "profile/<int:pk>/update/",
        user_views.ProfileUpdateView.as_view(),
        name="update_profile",
    ),
    path(
        "reset_password/",
        user_views.CustomPasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        user_views.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        user_views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        user_views.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "change_password/",
        user_views.CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
    path(
        "profile/<int:pk>/update_leagues/",
        user_views.ProfileUpdateFollowedLeaguesView.as_view(),
        name="update_leagues",
    ),
    path(
        "profile/<int:pk>/update_teams/",
        user_views.ProfileUpdateFollowedTeamsView.as_view(),
        name="update_teams",
    ),
]
