import mock
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files import File
from users.models import Profile


class TestProfileModel(TestCase):
    def setUp(self):
        self.mocked_image = mock.MagicMock(spec=File, name="FileMock")
        self.test_user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        Profile.objects.filter(user=self.test_user).update(image=self.mocked_image)
        self.expected_profile = Profile.objects.get(user=self.test_user)

    def test_profile_model_content(self):
        self.assertIsNotNone(self.test_user.profile)
        self.assertEqual(self.expected_profile.image.name, f"{self.mocked_image}")
