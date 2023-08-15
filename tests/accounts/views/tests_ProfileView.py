from django.test import TestCase, RequestFactory
from django.urls import reverse
from charity_app.accounts.models import CharityUserProfile
from charity_app.accounts.views import ProfileView
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class ProfileViewTest(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = self._create_user_with_valid_values()
        self.profile = CharityUserProfile.objects.get(user=self.user)

        self.view = ProfileView()
        self.view.object = self.profile
        self.view.user = self.user

    def test__get_context_data__expect_correct(self):
        request = self.factory.get(reverse('profile-user', kwargs={'pk': self.profile.user.pk}))
        response = ProfileView.as_view()(request, pk=self.profile.user.pk)
        context = response.context_data

        self.assertIn('charityuserprofile', context)
        self.assertEqual(context['charityuserprofile'], self.profile)
