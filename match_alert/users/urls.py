from django.urls import path
from users.views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    ProfileUpdateView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile"),
    path(
        "profile/<int:pk>/update/", ProfileUpdateView.as_view(), name="update_profile"
    ),
]
