from django.test import TestCase
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from users.signals import create_profile, save_profile


class TestSignals(TestCase):
    def setUp(self):
        post_save.disconnect(create_profile, sender=User)
        post_save.disconnect(save_profile, sender=User)

    def tearDown(self):
        post_save.connect(create_profile, sender=User)
        post_save.connect(save_profile, sender=User)

    def test_signal_creates_profile_after_user_creation(self):
        user = self.test_user = User.objects.create_user(
            username="user", password="StrongPassword1!"
        )
        create_profile(sender=User, instance=user, created=True)
        save_profile(sender=User, instance=user)
        self.assertIsNotNone(user.profile)
