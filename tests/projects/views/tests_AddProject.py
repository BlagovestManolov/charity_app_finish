from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse

from charity_app.projects.forms import AddProjectForm
from charity_app.projects.models import ProjectImages, Project
from charity_app.projects.views import AddProject

UserModel = get_user_model()


class AddProjectTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email="test@example.com",
            user_type="O",
        )

        self.client.login(username='testuser', password='testpassword')

        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

    def test__get_context_data__expect_correct(self):
        response = self.client.get(reverse('add-project'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('formset' in response.context)

    def test__form_invalid__expect_raise(self):
        form_data = {
            'project_name': 'Something111',
            'project_description': 'This is valid',
            'project_type': 'LFV',
        }

        response = self.client.post(reverse('add-project'), data=form_data, follow=True)
        self.assertFalse(Project.objects.exists())
        self.assertFalse(ProjectImages.objects.exists())

    def test__get_success_url__expect_redirect(self):
        project = Project.objects.create(organization=self.user)
        view = AddProject()
        view.object = project
        url = view.get_success_url()
        self.assertEqual(url, reverse('organization-finish-user', kwargs={'pk': project.organization_id}))

    def test__image_upload__expect_upload(self):
        formset_data = {
            'images-TOTAL_FORMS': 1,
            'images-INITIAL_FORMS': 0,
            'images-MAX_NUM_FORMS': 1000,
            'images-0-image': self.image,
        }

        response = self.client.post(reverse('add-project'), data=formset_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test__image_upload_invalid__expect_raise(self):
        formset_data = {
            'images-TOTAL_FORMS': 1,
            'images-INITIAL_FORMS': 0,
            'images-MAX_NUM_FORMS': 1000,
            # Missing image data or invalid image data
        }
        response = self.client.post(reverse('add-project'), data=formset_data, follow=True)  # Adjust the URL name
        self.assertEqual(response.status_code, 200)  # Check the expected response status code
        self.assertFalse(ProjectImages.objects.exists())