from django.urls import path
from users.views import auth, profile, password_management

urlpatterns = [
    path("register/", auth.RegisterView.as_view(), name="register"),
    path("login/", auth.CustomLoginView.as_view(), name="login"),
    path("logout/", auth.CustomLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", profile.ProfileView.as_view(), name="profile"),
    path(
        "profile/<int:pk>/update/",
        profile.ProfileUpdateView.as_view(),
        name="update_profile",
    ),
    path(
        "profile/<int:pk>/update_leagues/",
        profile.ProfileUpdateFollowedLeaguesView.as_view(),
        name="update_leagues",
    ),
    path(
        "profile/<int:pk>/update_teams/",
        profile.ProfileUpdateFollowedTeamsView.as_view(),
        name="update_teams",
    ),
    path(
        "reset_password/",
        password_management.CustomPasswordResetView.as_view(),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        password_management.CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        password_management.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        password_management.CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "change_password/",
        password_management.CustomPasswordChangeView.as_view(),
        name="change_password",
    ),
]
