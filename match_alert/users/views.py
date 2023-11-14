from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from home.models import League
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")
    success_message = "You have been successfully signed in!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        return context


class CustomLoginView(SuccessMessageMixin, LoginView):
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


class CustomLogoutView(LogoutView):
    template_name = "users/logout.html"
    extra_context = {"leagues": League.objects.all()}
