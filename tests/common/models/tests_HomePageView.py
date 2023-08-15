from django.core.exceptions import ValidationError
from django.test import TestCase

from django.urls import reverse

from charity_app.accounts.models import CharityUser
from charity_app.blogs.models import Blogs
from charity_app.common.views import HomePageView
from charity_app.projects.models import Project
from tests.common.models.create_objects_mixin import CreateObjectsMixin


class HomePageTest(CreateObjectsMixin, TestCase):
    view = HomePageView()

    def setUp(self) -> None:
        self.url = reverse('index')

    def test__response_code__expect_correct(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test__get_n_random_objects__valid_data_with_one_user__expect_to_be_posted(self):
        # Create user with valid information
        self._create_user_with_valid_values_one()

        random_user = self.view._get_n_random_objects_from_model(
            CharityUser,
            1,
            is_staff=False,
            user_type='U',
        )

        self.assertEquals(len(random_user), 1)
        self.assertTrue(all(isinstance(user, CharityUser) for user in random_user))

    def test__get_n_random_objects__valid_data_with_two_or_more_user__expect_to_be_posted(self):
        # Create two users with valid data
        self._create_user_with_valid_values_one()
        self._create_user_with_valid_values_two()

        random_user = self.view._get_n_random_objects_from_model(
            CharityUser,
            2,
            is_staff=False,
            user_type='U',
        )

        self.assertEquals(len(random_user), 2)
        self.assertTrue(all(isinstance(user, CharityUser) for user in random_user))

    def test__get_n_random_objects__valid_data_with_one_object_but_with_two_number_of_objects__expect_to_be_posted(
            self):
        # Create users

        self._create_project_with_project_type_LFV()
        self._create_project_with_project_type_SMA()

        random_project = self.view._get_n_random_objects_from_model(
            Project,
            3,
            project_type='LFV',
        )

        self.assertEquals(len(random_project), 1)
        self.assertTrue(all(isinstance(project, Project) for project in random_project))

    def test__get_objects_from_model__valid_data__expect_to_be_posted(self):
        self._create_organization_valid_vales()
        self._create_organization_valid_values_two()

        all_organizations = self.view._get_objects_from_model(CharityUser)
        self.assertEquals(len(all_organizations), 2)
        self.assertTrue(all(isinstance(organization, CharityUser) for organization in all_organizations))

    def test__add_to_context__valid_data__expect_to_be_posted(self):
        context = self.view._add_to_context(key1='test one', key2='test two')

        self.assertEquals(context['key1'], 'test one')
        self.assertEquals(context['key2'], 'test two')

