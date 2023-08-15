from django.contrib.auth import get_user_model
from django.test import TestCase

from charity_app.blogs.models import Blogs
from charity_app.blogs.views import BlogsView
from charity_app.projects.models import Project

UserModel = get_user_model()


class BlogsViewTest(TestCase):
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

        self.blog_one = Blogs.objects.create(
            project=self.project,
            blog_title='One Blog',
        )

        self.blog_two = Blogs.objects.create(
            project=self.project,
            blog_title='Two Blog',
        )

    def test__get_queryset__expect_get_it(self):
        view = BlogsView()
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.blog_one, queryset)
        self.assertIn(self.blog_two, queryset)
        self.assertEqual(queryset.first(), self.blog_one)


