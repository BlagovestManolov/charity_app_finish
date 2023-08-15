from django.test import TestCase
from django.urls import reverse

from charity_app.accounts.models import OrganizationUserProfile
from charity_app.accounts.views import OrganizationUserView
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class OrganizationUserViewTest(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.user = self._create_organization_valid_values()
        self.profile = OrganizationUserProfile.objects.get(user=self.user)

    def test_get_success_url__expect_correct(self):
        view = OrganizationUserView()
        view.object = self.profile

        success_url = view.get_success_url()
        expected_url = reverse('organization-finish-user', kwargs={'pk': self.profile.user.pk})

        self.assertEqual(success_url, expected_url)
