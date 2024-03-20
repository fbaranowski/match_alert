from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from home.models import League, Team
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TestRegisterView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("register"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/register/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/register.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<button class="btn btn-outline-info" type="submit">Sign Up</button>',
        )

    def test_post_request_creates_new_user(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": "test",
                "last_name": "test",
                "username": "test_user",
                "email": "test@gmail.com",
                "password1": "StrongPassword123!",
                "password2": "StrongPassword123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(first_name="test").exists())


class TestCustomLoginView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("login"))

    def test_url_at_correct_endpoint(self):
        self.response = self.client.get("/auth/login/")
        self.assertEqual(self.response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/login.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<button class="btn btn-outline-info" type="submit">Log In</button>',
        )

    def test_post_request_logs_in_user(self):
        User.objects.create_user(username="user", password="StrongPassword1!")
        response = self.client.post(
            reverse("login"), data={"username": "user", "password": "StrongPassword1!"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user(self.client).is_authenticated)


class TestCustomLogoutView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("logout"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/logout/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/logout.html")

    def test_template_content(self):
        self.assertContains(self.response, "<p>You have been logged out</p>")


class TestProfileView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        self.client.login(username="user", password="StrongPassword1!")
        self.response = self.client.get(reverse("profile", kwargs={"pk": self.user.pk}))

    def test_url_at_correct_endpoint(self):
        response = self.client.get(f"/auth/profile/{self.user.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/profile.html")

    def test_template_content(self):
        self.assertContains(
            self.response, '<p class="follow-header">Available options:</p>'
        )

    def test_user_has_no_access_to_another_user_profile(self):
        second_user = User.objects.create_user(username="user2", password="user2pass")
        response = self.client.get(reverse("profile", kwargs={"pk": second_user.pk}))
        self.assertEqual(response.status_code, 302)


class TestProfileUpdateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        self.client.login(username="user", password="StrongPassword1!")
        self.response = self.client.get(
            reverse("update_profile", kwargs={"pk": self.user.pk})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get(f"/auth/profile/{self.user.pk}/update/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/update_profile.html")

    def test_template_content(self):
        self.assertContains(
            self.response, '<legend class="border-bottom mb-4">Update profile</legend>'
        )

    def test_post_request_updates_profile(self):
        response = self.client.post(
            reverse("update_profile", kwargs={"pk": self.user.pk}),
            data={
                "username": "test",
                "email": "test@wp.pl",
                "first_name": "test",
                "last_name": "test",
                "update": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, "test")


class TestProfileUpdateFollowedLeaguesView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        self.client.login(username="user", password="StrongPassword1!")
        self.response = self.client.get(
            reverse("update_leagues", kwargs={"pk": self.user.pk})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get(f"/auth/profile/{self.user.pk}/update_leagues/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/update_followed_leagues.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<legend class="border-bottom mb-4">Change followed leagues</legend>',
        )

    def test_post_request_updates_followed_leagues(self):
        league_to_follow = League.objects.create(name="test_league")
        response = self.client.post(
            reverse("update_leagues", kwargs={"pk": self.user.pk}),
            data={"leagues": [league_to_follow]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.profile.leagues, league_to_follow)


class TestProfileUpdateFollowedTeamsView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        self.client.login(username="user", password="StrongPassword1!")
        self.response = self.client.get(
            reverse("update_teams", kwargs={"pk": self.user.pk})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get(f"/auth/profile/{self.user.pk}/update_teams/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/update_followed_teams.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<legend class="border-bottom mb-4">Change followed teams</legend>',
        )

    def test_post_request_updates_followed_teams(self):
        test_league = League.objects.create(name="test_league")
        team_to_follow = Team.objects.create(name="test_team", league=test_league)
        response = self.client.post(
            reverse("update_teams", kwargs={"pk": self.user.pk}),
            data={"teams": [team_to_follow]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.profile.teams, team_to_follow)


class TestCustomPasswordResetView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("reset_password"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/reset_password/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/reset_password.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<button class="btn btn-outline-info" type="submit">Send e-mail</button>',
        )

    def test_post_request(self):
        response = self.client.post(
            reverse("reset_password"), data={"email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 302)


class TestCustomPasswordResetDoneView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("password_reset_done"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/reset_password_sent/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/password_reset_sent.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>Password Reset Sent</h1>")


class TestCustomPasswordResetConfirmView(TestCase):
    def test_get_and_post_requests(self):
        user = User.objects.create_user(username="user", password="StrongPassword1!")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(
            reverse("password_reset_confirm", kwargs={"token": token, "uidb64": uid})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("users/password_reset_confirm.html")

        response = self.client.post(
            reverse("password_reset_confirm", kwargs={"token": token, "uidb64": uid}),
            data={"new_password1": "pass", "new_password2": "pass"},
        )
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(id=user.id)
        self.assertTrue(updated_user.password, "pass")


class TestCustomPasswordResetCompleteView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("password_reset_complete"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/reset_password_complete/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/password_reset_done.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>Password Reset Complete</h1>")


class TestChangePasswordView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        self.client.login(username="user", password="StrongPassword1!")
        self.response = self.client.get(reverse("change_password"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/auth/change_password/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "users/change_password.html")

    def test_template_content(self):
        self.assertContains(
            self.response,
            '<legend class="border-bottom mb-4">Change Your Password</legend>',
        )

    def test_post_request_changes_password(self):
        response = self.client.post(
            reverse("change_password"),
            data={"new_password1": "new_password", "new_password2": "new_password"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.password, "new_password")
