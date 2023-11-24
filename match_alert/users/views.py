from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from users.forms import UserRegisterForm
from home.models import League
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    success_message = "You have been successfully signed in!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomLoginView(SuccessMessageMixin, auth_views.LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("home")
    success_message = "You have been successfully logged in!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return redirect("login")


class CustomLogoutView(auth_views.LogoutView):
    template_name = "users/logout.html"
    extra_context = {"leagues": League.objects.all()}


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

        return redirect("home")

    def test_func(self):
        user = User.objects.get(pk=self.kwargs["pk"])
        return self.request.user == user

    def handle_no_permission(self):
        messages.error(self.request, "You have no access to this page")
        return redirect("home")


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = "users/reset_password.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "users/password_reset_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "users/password_reset_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "users/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomPasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "users/change_password.html"
    extra_context = {"leagues": League.objects.all()}
    success_url = reverse_lazy("home")
    success_message = "Your password has been changed"
