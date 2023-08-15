from django.test import TestCase
from django.urls import reverse

from charity_app.accounts.models import CharityUserProfile
from charity_app.accounts.views import ProfileUserView
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class ProfileUserViewTest(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.user = self._create_user_with_valid_values()
        self.profile = CharityUserProfile.objects.get(user=self.user)

    def test_get_success_url__expect_correct(self):
        view = ProfileUserView()
        view.object = self.profile

        success_url = view.get_success_url()
        expected_url = reverse('profile-finish-user', kwargs={'pk': self.profile.user.pk})

        self.assertEqual(success_url, expected_url)
