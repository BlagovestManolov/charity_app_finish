from django.test import TestCase
from django.urls import reverse

from charity_app.projects.models import Project
from tests.common.models.create_objects_mixin import CreateObjectsMixin
from charity_app.common.views import DonationView


class VolunteerTest(CreateObjectsMixin, TestCase):
    volunteer = DonationView()

    def setUp(self) -> None:
        self.url = reverse('donation')

        self.user = self._create_user_with_valid_values_one()

    def test__response_code__expect_correct(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test__template_used__expect_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'common/donation-page.html')

    def test__queryset_filtering__expect_correct(self):
        project1 = Project.objects.create(
            organization=self.user,
            project_name='Project 1',
            project_type='SFA',
            is_active=True,
        )
        project2 = Project.objects.create(
            organization=self.user,
            project_name='Project 2',
            project_type='LFV',
            is_active=True,
        )
        project3 = Project.objects.create(
            organization=self.user,
            project_name='Project 3',
            project_type='SMA',
            is_active=True,
        )
        project4 = Project.objects.create(
            organization=self.user,
            project_name='Project 4',
            project_type='SFA',
            is_active=False,  # Not active
        )

        response = self.client.get(self.url)
        self.assertIn('projects', response.context)
        projects = response.context['projects']
        self.assertEqual(projects.count(), 1)
        self.assertIn(project1, projects)
        self.assertNotIn(project2, projects)
        self.assertNotIn(project3, projects)
        self.assertNotIn(project4, projects)