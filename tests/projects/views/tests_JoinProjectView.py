from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from charity_app.projects.models import Project

UserModel = get_user_model()


class JoinProjectViewTest(TestCase):
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

