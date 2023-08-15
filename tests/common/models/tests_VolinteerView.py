from django.test import TestCase
from django.urls import reverse

from charity_app.projects.models import Project
from tests.common.models.create_objects_mixin import CreateObjectsMixin
from charity_app.common.views import VolunteerView


class VolunteerTest(CreateObjectsMixin, TestCase):
    volunteer = VolunteerView()

    def setUp(self) -> None:
        self.url = reverse('become-volunteer')

        self.user = self._create_user_with_valid_values_one()

    def test__response_code__expect_correct(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test__template_used__expect_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'common/volunteer-page.html')

    def test__queryset_filtering__expect_correct(self):
        project1 = Project.objects.create(
            organization=self.user,
            project_name='Project 1',
            project_type='LFV',
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
            project_type='SMA',  # Not 'LFV'
            is_active=True,
        )
        project4 = Project.objects.create(
            organization=self.user,
            project_name='Project 4',
            project_type='LFV',
            is_active=False,  # Not active
        )

        response = self.client.get(self.url)
        self.assertIn('projects', response.context)
        projects = response.context['projects']
        self.assertEqual(projects.count(), 2)  # Only active LFV projects
        self.assertIn(project1, projects)
        self.assertIn(project2, projects)
        self.assertNotIn(project3, projects)  # Should not be included due to project type
        self.assertNotIn(project4, projects)