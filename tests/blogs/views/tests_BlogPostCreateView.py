from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from charity_app.blogs.forms import BlogPostForm
from charity_app.blogs.models import Blogs
from charity_app.blogs.views import BlogPostCreateView
from charity_app.projects.models import Project

UserModel = get_user_model()


class BlogPostCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

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

        self.response = self.client.get(reverse('add-blog'))

    def test__create_view_with_authenticated_organization__expect_correct_response_code_and_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add-blog'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/create-blog-page.html')

    def test__create_view_with_instances__expect_correct(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add-blog'))

        self.assertIsInstance(response.context['view'], BlogPostCreateView)
        self.assertIsInstance(response.context['form'], BlogPostForm)

    def test__form_valid(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'project': self.project.id,
            'blog_title': 'Test Title',
            'blog_information': 'Test information',
        }

        self.client.post(reverse('add-blog'), data=form_data)

        self.assertTrue(Blogs.objects.filter(blog_title='Test Title').exists())
        new_blog = Blogs.objects.get(blog_title='Test Title')
        self.assertEqual(new_blog.project, self.project)

