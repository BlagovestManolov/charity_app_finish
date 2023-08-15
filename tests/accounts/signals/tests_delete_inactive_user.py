from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from charity_app.accounts.models import OrganizationUserProfile, CharityUserProfile
from charity_app.accounts.signals import delete__user_profile_related_to_the_deleted_user
from charity_app.blogs.models import Blogs, BlogComments
from charity_app.projects.models import Project, ProjectImages
from tests.accounts.models.mixin import CreateProfileObjectsMixin

UserModel = get_user_model()


class TestUserSignal(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(
            username='testuser',
            password='testpassword',
            email="test@example.com",
            user_type="O",
        )

        # Create a project and related objects
        self.project = Project.objects.create(
            organization=self.user,
            project_name="Test Project",
            project_description='This is some random text',
            project_type='LFV',
            is_active=True,
        )

        self.image = ProjectImages.objects.create(
            project=self.project)

        self.blog = Blogs.objects.create(project=self.project, blog_title="Test Blog")

        self.comment = BlogComments.objects.create(blog=self.blog, user=self.user, content="Test Comment")

    def test__user_last_login_date__expect_correct(self):
        last_login_before = self.user.last_login
        self.client.login(
            username='testuser',
            password='testpassword',
        )

        self.user.refresh_from_db()
        last_login_after = self.user.last_login

        self.assertNotEqual(last_login_after, last_login_before)

    def test__delete_user_automatically_if_inactive_more_than_365_days__expect_delete(self):
        self.user.last_login = timezone.now() - timezone.timedelta(days=400)
        self.user.save()
        self.assertFalse(UserModel.objects.filter(username='testuser').exists())

    def test__delete_user_automatically_if_active_small_than_365_days__expect_not_delete(self):
        self.user.last_login = timezone.now() - timezone.timedelta(days=100)
        self.user.save()
        self.assertTrue(UserModel.objects.filter(username='testuser').exists())

    def test__delete_user_profile__expect_deleted(self):
        self.user.last_login = timezone.now() - timezone.timedelta(days=400)
        self.user.save()

        self.assertEqual(OrganizationUserProfile.objects.filter(user=self.user).count(), 0)

    def test__created_all_objects__expected_to_be_created(self):
        self.assertEqual(Project.objects.filter(organization=self.user).count(), 1)
        self.assertEqual(ProjectImages.objects.filter(project=self.project).count(), 1)
        self.assertEqual(Blogs.objects.filter(project=self.project).count(), 1)
        self.assertEqual(BlogComments.objects.filter(blog=self.blog).count(), 1)

    def test__delete_project_blog_and_more__expect_deleted(self):
        self.user.last_login = timezone.now() - timezone.timedelta(days=400)
        self.user.save()

        self.assertEqual(Project.objects.filter(organization=self.user).count(), 0)
        self.assertEqual(ProjectImages.objects.filter(project=self.project).count(), 0)
        self.assertEqual(Blogs.objects.filter(project=self.project).count(), 0)
        self.assertEqual(BlogComments.objects.filter(blog=self.blog).count(), 0)
        self.assertEqual(self.project.volunteers.count(), 0)


class DeleteUserTest(TestCase):
    def setUp(self) -> None:
        self.organization = UserModel.objects.create_user(
            username='testorganization',
            password='testpassword',
            email="test@example.com",
            user_type="O",
        )

        self.volunteer = UserModel.objects.create_user(
            username='testuser',
            password='passwordtest',
            email='user@gmail.com',
            user_type='U',
        )

    def test__organization_profile_not_deleted_user__expect_to_be_created(self):
        self.assertEqual(OrganizationUserProfile.objects.filter(user=self.organization).count(), 1)

    def test__organization_profile_deleted_user__expect_to_be_deleted(self):
        self.organization.delete()
        self.assertEqual(OrganizationUserProfile.objects.filter(user=self.organization).count(), 0)

    def test__volunteer_profile_not_deleted_user__expect_to_be_created(self):
        self.assertEqual(CharityUserProfile.objects.filter(user=self.volunteer).count(), 1)

    def test__volunteer_profile_deleted_user__expect_to_be_deleted(self):
        self.volunteer.delete()
        self.assertEqual(CharityUserProfile.objects.filter(user=self.volunteer).count(), 0)

