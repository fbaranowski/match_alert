import mock
from django.core.files import File
from django.test import TestCase
import users.forms as forms
from home.models import League, Team


class TestUserRegisterForm(TestCase):
    def test_user_register_form_with_valid_data(self):
        form = forms.UserRegisterForm(
            data={
                "first_name": "test",
                "last_name": "test",
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_register_form_no_data(self):
        form = forms.UserRegisterForm(data={})
        self.assertFalse(form.is_valid())


class TestUserUpdateForm(TestCase):
    def test_user_update_form_with_valid_data(self):
        form = forms.UserUpdateForm(
            data={
                "username": "test_user",
                "email": "test@gmail.com",
                "first_name": "test",
                "last_name": "test",
            }
        )
        self.assertTrue(form.is_valid())

    def test_user_update_form_with_no_data(self):
        form = forms.UserUpdateForm(data={})
        self.assertFalse(form.is_valid())


class TestProfileUpdateForm(TestCase):
    def test_profile_update_form_with_valid_data(self):
        form = forms.ProfileUpdateForm(
            data={"image": mock.MagicMock(spec=File, name="FileMock")}
        )
        self.assertTrue(form.is_valid())

    def test_profile_update_form_with_no_data(self):
        form = forms.ProfileUpdateForm(data={})
        self.assertTrue(form.is_valid())


class TestProfileLeagueForm(TestCase):
    def test_profile_league_form_with_valid_data(self):
        league_to_follow1 = League.objects.create(name="test_league")
        league_to_follow2 = League.objects.create(name="test_league2")
        form = forms.ProfileLeagueForm(
            data={"leagues": [league_to_follow1, league_to_follow2]}
        )
        self.assertTrue(form.is_valid())

    def test_profile_league_with_no_data(self):
        form = forms.ProfileLeagueForm(data={})
        self.assertTrue(form.is_valid())


class TestProfileTeamForm(TestCase):
    def test_profile_team_form_with_valid_data(self):
        test_league = League.objects.create(name="test_league")
        team_to_follow1 = Team.objects.create(name="test_team1", league=test_league)
        team_to_follow2 = Team.objects.create(name="test_team2", league=test_league)
        form = forms.ProfileTeamForm(data={"teams": [team_to_follow1, team_to_follow2]})
        self.assertTrue(form.is_valid())

    def test_profile_team_with_no_data(self):
        form = forms.ProfileTeamForm(data={})
        self.assertTrue(form.is_valid())
