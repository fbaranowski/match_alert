from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from users.models import Profile
from home.models import League, Team


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class ProfileLeagueForm(forms.ModelForm):
    leagues = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=League.objects.all(),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ["leagues"]


class ProfileTeamForm(forms.ModelForm):
    leagues = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Team.objects.all(), required=False
    )

    class Meta:
        model = Profile
        fields = ["teams"]
