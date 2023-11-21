from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from users.forms import UserRegisterForm
from home.models import League
from django.contrib.auth.views import LoginView, LogoutView, TemplateView
from django.contrib import messages
from users.models import Profile
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


# class ProfileView(View, LoginRequiredMixin, UserPassesTestMixin):
#     template_name = 'users/update_profile.html'
#     user_form_class = UserUpdateForm
#     profile_form_class = ProfileUpdateForm
#     initial = {"key": "value"}
#     model = Profile
#
#     def get(self, request, *args, **kwargs):
#         user_form = self.user_form_class(initial=self.initial)
#         profile_form = self.profile_form_class(initial=self.initial)
#         return render(request, self.template_name,
#                       {"user_form": user_form, "profile_form": profile_form})
#
#     def post(self, request, *args, **kwargs):
#         user_form = self.user_form_class(request.POST)
#         profile_form = self.profile_form_class(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Your profile has been updated")
#             return redirect('home')
#
# return render(request, self.template_name,
#               {"user_form": user_form, "profile_form": profile_form})
#
#     def test_func(self):
#         profile = self.get_object()
#         return self.request.user == profile.user


# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = User
#     fields = ['username', 'email']
#     context_object_name = 'user'
#     template_name = 'users/update_profile.html'
#     success_url = '/'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProfileUpdateView, self).get_context_data(**kwargs)
#         context['profile'] = Profile.objects.get(pk=self.request.user.id).image
#         context['leagues'] = League.objects.all()
#         return context


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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
        get_object_or_404(Profile, user__pk=pk)
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
