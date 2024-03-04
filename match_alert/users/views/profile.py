from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from home.models import League
from users.forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    ProfileLeagueForm,
    ProfileTeamForm,
)


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, auth_views.TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        context["user"] = user
        context["profile"] = user.profile
        context["leagues"] = League.objects.all()
        return context

    def test_func(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, "You have no access to this page")
        return redirect("home")


class ProfileUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, auth_views.TemplateView
):
    template_name = "users/update_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        context["user"] = user
        context["user_form"] = UserUpdateForm(instance=user)
        context["profile_form"] = ProfileUpdateForm(instance=user.profile)
        context["leagues"] = League.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile
        )
        if "update" in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated")
            else:
                messages.error(request, "Invalid form - could not update the profile")
        return redirect("profile", pk=user.pk)

    def test_func(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, "You have no access to this page")
        return redirect("home")


class ProfileUpdateFollowedLeaguesView(
    auth_views.TemplateView, LoginRequiredMixin, UserPassesTestMixin
):
    template_name = "users/update_followed_leagues.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        context["leagues"] = League.objects.all()
        context["form"] = ProfileLeagueForm(instance=user.profile)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        form = ProfileLeagueForm(request.POST, instance=user.profile)
        if "update" in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "You have updated followed leagues")
            else:
                messages.error(
                    request, "Invalid form - could not update followed leagues"
                )
        return redirect("profile", pk=user.pk)

    def test_func(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, "You have no access to this page")
        return redirect("home")


class ProfileUpdateFollowedTeamsView(
    auth_views.TemplateView, LoginRequiredMixin, UserPassesTestMixin
):
    template_name = "users/update_followed_teams.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        context["leagues"] = League.objects.all()
        context["form"] = ProfileTeamForm(instance=user.profile)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        user = get_object_or_404(User, pk=pk)
        form = ProfileTeamForm(request.POST, instance=user.profile)
        if "update" in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, "You have updated followed teams")
            else:
                messages.error(
                    request, "Invalid form - could not update followed teams"
                )
        return redirect("profile", pk=user.pk)

    def test_func(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, "You have no access to this page")
        return redirect("home")
