from charity_app.accounts.models import CharityUser
from charity_app.blogs.models import Blogs
from charity_app.projects.models import Project


class CreateObjectsMixin:
    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test_user@gmail.com',
        'password': 'testpassword',
        'user_type': 'U',
    }

    VALID_PROJECT_DATA = {
        'project_name': 'Test Project',
        'project_description': 'Test description',
        'project_type': 'LFV',
    }

    VALID_BLOG_DATA = {
        'blog_title': 'Test Blog',
        'blog_information': 'Test information',
    }

    def _create_user_with_valid_values_one(self):
        return CharityUser.objects.create_user(
            **self.VALID_USER_DATA,
        )

    @staticmethod
    def _create_user_with_valid_values_two():
        return CharityUser.objects.create_user(
            username='testtwo',
            email='test_two@gmail.com',
            password='testTwo',
            user_type='U',
        )

    @staticmethod
    def _create_user_with_same_email_as_user_two():
        return CharityUser.objects.create_user(
            username='testthree',
            email='test_two@gmail.com',
            password='testThree',
            user_type='U',
        )

    def _create_user_with_is_staff_true(self):
        return CharityUser.objects.create_user(
            **self.VALID_USER_DATA,
            is_staff=True,
        )

    @staticmethod
    def _create_organization_valid_vales():
        return CharityUser.objects.create_user(
            username='Organization',
            email='organization@gmail.com',
            password='Organization',
            user_type='O',
        )

    @staticmethod
    def _create_organization_valid_values_two():
        return CharityUser.objects.create_user(
            username='Organiztwo',
            email='organtwo@gmail.com',
            password='Organtwo',
            user_type='O',
        )

    def _create_user_with_invalid_is_staff_value(self):
        return CharityUser.objects.create_user(
            **self.VALID_USER_DATA,
            is_staff=False,
        )

    def _create_project_with_project_type_LFV(self):
        return Project.objects.create(
            organization_id=self._create_organization_valid_vales().pk,
            **self.VALID_PROJECT_DATA,
            is_active=True,
        )

    def _create_project_with_project_type_SMA(self):
        return Project.objects.create(
            organization_id=self._create_organization_valid_values_two().pk,
            project_name='Test Project',
            project_description='Test project description',
            project_type='SMA',
            is_active=True,
        )

    def _create_blog_one(self):
        return Blogs.objects.create(
            project_id=self._create_project_with_project_type_SMA().pk,
            **self.VALID_BLOG_DATA,
        )

    def _create_blog_two(self):
        return Blogs.objects.create(
            project_id=self._create_project_with_project_type_LFV().pk,
            blog_title='Test two title',
            blog_information='Test two blog information',
        )

