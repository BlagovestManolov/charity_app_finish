from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from charity_app.blogs.models import Blogs, BlogComments
from charity_app.blogs.views import CommentCreateView
from charity_app.projects.models import Project

UserModel = get_user_model()


class CommentCreateViewTest(TestCase):
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

        self.client = Client()

    def test__form_valid__expect_validate(self):
        self.client.login(username='testuser', password='testpassword')

        form_data = {
            'blog': self.blog_one,
            'user': self.user,
            'content': 'This is a text!'
        }

        response = self.client.post(reverse('add-comment', args=[self.blog_one.pk]), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogComments.objects.count(), 1)
        first_comment = BlogComments.objects.first()

        self.assertEqual(first_comment.content, 'This is a text!')
        self.assertEqual(first_comment.user, self.user)
        self.assertEqual(first_comment.blog, self.blog_one)

    def test__get_success_url__expect_go_to_the_specific_page(self):
        view = CommentCreateView()
        success_url = view.get_success_url()
        self.assertEqual(success_url, reverse('blog-list'))