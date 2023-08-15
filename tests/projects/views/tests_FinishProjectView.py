from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from charity_app.projects.models import Project
from charity_app.projects.views import FinishProjectView

UserModel = get_user_model()


class FinishProjectViewTest(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email="test@example.com",
            user_type="O",
        )

        self.project = Project.objects.create(
            organization=self.user,
            project_name="Test Project",
            project_description='This is some random text',
            project_type='LFV',
            is_active=True,
        )

    def test__redirect_url__expect_redirect(self):
        view = FinishProjectView()
        view.kwargs = {'pk': self.project.pk}

        redirect_url = view.get_redirect_url()
        expected_url = reverse('organization-finish-user', kwargs={'pk': self.project.organization_id})
        self.assertEqual(redirect_url, expected_url)

    def test__get_method__expect_correct(self):
        view = FinishProjectView()
        view.kwargs = {'pk': self.project.pk}

        response = view.get(self.project)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('organization-finish-user', kwargs={'pk': self.project.organization_id}))
        self.assertFalse(Project.objects.get(pk=self.project.pk).is_active)