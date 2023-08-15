from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from charity_app.blogs.forms import BlogPostForm
from charity_app.blogs.models import Blogs
from charity_app.projects.models import Project

UserModel = get_user_model()


class BlogPostFormTest(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email="test@example.com",
            user_type="O",
        )

        # Create a project and related objects
        self.project_one = Project.objects.create(
            organization=self.user,
            project_name="Test Project",
            project_description='This is some random text',
            project_type='LFV',
            is_active=True,
        )

        self.project_two = Project.objects.create(
            organization=self.user,
            project_name="Two Project",
            project_description='This is some random text two',
            project_type='LFV',
            is_active=True,
        )

        self.blog_one = Blogs.objects.create(
            project=self.project_one,
            blog_title='Title one',
        )

        self.blog_two = Blogs.objects.create(
            project=self.project_two,
            blog_title='Title two',
        )

    def test__form_with_user_projects__expect_post(self):
        user_projects = Blogs.objects.all()[:2]

        form = BlogPostForm(user_projects=user_projects)

        self.assertIsInstance(form.fields['project'], forms.ModelChoiceField)
        self.assertEqual(list(form.fields['project'].queryset), list(user_projects))
        self.assertEqual(form.fields['project'].label, 'Select a Project')

    def test__form_without_user_projects__expect_not_post(self):
        self.project_one.delete()
        self.project_two.delete()
        form = BlogPostForm()

        self.assertIsInstance(form.fields['project'], forms.ModelChoiceField)
        self.assertEqual(form.fields['project'].label, 'Project')

    def test__form_validation__expect_validation(self):
        form_data = {
            'project': self.project_one.id,
            'blog_title': 'Test Title',
            'blog_information': 'Test Info',
        }

        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data_missing = {
            'blog_title': 'Test Title',
            'blog_information': 'Test Info Two',
        }

        form_missing_project = BlogPostForm(data=form_data_missing)
        self.assertFalse(form_missing_project.is_valid())
