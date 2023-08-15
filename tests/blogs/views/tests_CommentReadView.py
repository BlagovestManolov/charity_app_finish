from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from charity_app.blogs.models import Blogs, BlogComments
from charity_app.blogs.views import CommentReadView
from charity_app.projects.models import Project

UserModel = get_user_model()


class CommentReadViewTest(TestCase):
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

        self.comment_one = BlogComments.objects.create(
            blog=self.blog_one,
            user=self.user,
            content='This is some test!',
        )

        self.comment_two = BlogComments.objects.create(
            blog=self.blog_one,
            user=self.user,
            content='This is some text two!',
        )

    def test__get_queryset__expect_get_it(self):
        view = CommentReadView()
        view.kwargs = {'blog_id': self.blog_one.pk}
        queryset = view.get_queryset()

        self.assertEqual(queryset.count(), 2)
        self.assertIn(self.comment_one, queryset)
        self.assertIn(self.comment_two, queryset)

    def test__get_context_data__expect_correct(self):
        response = self.client.get(reverse('read-comment', args=[self.blog_one.id]))

        self.assertEqual(response.status_code, 200)
        self.assertIn('blog_information', response.context)
        self.assertEqual(response.context['blog_information'], self.blog_one)
        self.assertIn('comments', response.context)
        self.assertEqual(len(response.context['comments']), 2)