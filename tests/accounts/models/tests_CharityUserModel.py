from django.test import TestCase

from charity_app.accounts.models import CharityUser, UserType
from tests.common.models.create_objects_mixin import CreateObjectsMixin


class CharityUserModelTest(CreateObjectsMixin, TestCase):

    def test__user_type_choices(self):
        user_type_choices = CharityUser._meta.get_field('user_type').choices
        enum_choices = [(choice.value, choice.name) for choice in UserType]
        self.assertEquals(user_type_choices, enum_choices)

    def test__user_type_max_len(self):
        max_len = CharityUser._meta.get_field('user_type').max_length
        enum_max_len = UserType.max_len()
        self.assertEquals(max_len, enum_max_len)

    def test__str_method_with_valid_data__expect_correct(self):
        user = self._create_user_with_valid_values_one()
        self.assertEquals(str(user), 'test_user@gmail.com')

    def test__email_unique_with_invalid_data__expect_raise(self):
        self._create_user_with_valid_values_two()
        with self.assertRaises(Exception):
            self._create_user_with_same_email_as_user_two()
