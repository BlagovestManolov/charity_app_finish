from django.test import TestCase, RequestFactory
from django.urls import reverse

from charity_app.accounts.views import OrganizationView
from charity_app.projects.models import Project
from tests.accounts.models.mixin import CreateProfileObjectsMixin
from charity_app.accounts.models import OrganizationUserProfile


class OrganizationViewTest(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = self._create_organization_valid_values()
        self.organization_profile = OrganizationUserProfile.objects.get(user=self.user)

        self.active_project = Project.objects.create(
            project_name='Test One',
            project_description='Some random text one',
            is_active=True,
            organization=self.user,
            project_type='LFV',
        )

        self.inactive_project = Project.objects.create(
            project_name='Test Two',
            project_description='Some random text two',
            is_active=False,
            organization=self.user,
            project_type='SMA',
        )

        self.view = OrganizationView()
        self.view.object = self.organization_profile
        self.view.user = self.user

    def test__get_context_data__expect_correct(self):
        request = self.factory.get(reverse('organization-user', kwargs={'pk': self.organization_profile.user.pk}))
        request.user = self.user
        response = OrganizationView.as_view()(request, pk=self.organization_profile.user.pk)
        context = response.context_data

        self.assertIn('organizationuserprofile', context)
        self.assertEqual(context['organizationuserprofile'], self.organization_profile)
        self.assertIn('project_organization_active', context)
        self.assertIn(self.active_project, context['project_organization_active'])
        self.assertNotIn(self.inactive_project, context['project_organization_active'])
        self.assertIn('project_organization_no_active', context)
        self.assertIn(self.inactive_project, context['project_organization_no_active'])
        self.assertNotIn(self.active_project, context['project_organization_no_active'])