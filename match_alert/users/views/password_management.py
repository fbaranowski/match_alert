from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from home.models import League


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
