from enum import Enum

from django.test import TestCase

from charity_app.accounts.mixins import ChoicesMixin, GetInformationFromModelMixin, GetCharityUserMixin
from charity_app.accounts.models import CharityUser
from charity_app.common.mixin import AddToContextMixin
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class UserMixinTest(CreateProfileObjectsMixin, TestCase):
    def setUp(self) -> None:
        self.user = self._create_user_with_valid_values()
        self.client.login(username='testuser', password='testpassword')

    def test__get_user_primary_key__expect_correct(self):
        mixin = GetInformationFromModelMixin()
        mixin.request = self.client.request().wsgi_request
        mixin.request.user = self.user

        primary_key = mixin._get_user_primary_key()
        self.assertEquals(primary_key, self.user.pk)

    def test__get_objects_from_model__all(self):
        # The first user coming from setUp built-in model
        self._create_user_with_valid_values_two()

        mixin = GetInformationFromModelMixin()
        mixin.request = self.client.request().wsgi_request

        objects = mixin._get_objects_from_model(CharityUser)
        self.assertEquals(objects.count(), 2)

    def test__get_objects_from_model_filtered(self):
        self._create_user_with_valid_values_two()

        mixin = GetInformationFromModelMixin()
        mixin.request = self.client.request().wsgi_request

        filtered_objects = mixin._get_objects_from_model(CharityUser, username='testwo')
        self.assertEqual(filtered_objects.count(), 1)


class MockDetailView(GetCharityUserMixin):
    def get_object(self):
        return self.request.user


class GetCharityUserTest(CreateProfileObjectsMixin, TestCase):

    def setUp(self) -> None:
        self.user = self._create_user_with_valid_values()
        self.client.login(username='testuser', password='testpassword')

    def test__get_user__expect_correct(self):
        mixin = MockDetailView()
        mixin.request = self.client.request().wsgi_request
        mixin.request.user = self.user

        returned_user = mixin._get_user()
        self.assertEqual(returned_user, self.user)


class AddToContextMixinTest(TestCase):

    def test__add_to_context__except_correct(self):
        mixin = AddToContextMixin()
        context = mixin._add_to_context(
            key1='1',
            key2='2',
        )

        self.assertEquals(context, {'key1': '1', 'key2':'2'})