from django.core.exceptions import ValidationError
from django.test import TestCase

from charity_app.accounts.models import CharityUserProfile, CharityUser
from charity_app.accounts.validators import name_validator, phone_number_validator
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class CharityUserProfileModelTest(CreateProfileObjectsMixin, TestCase):
    VALID_NAMES = [
        'Boby',
        'Dani',
        'Tanq',
    ]

    INVALID_NAMES = [
        'Bob1',
        '123Toni',
        '!Tanq',
    ]

    VALID_PHONE_NUMBERS = [
        '+359111222333',
        '+359111222331',
        '+359111222332',
    ]

    INVALID_PHONE_NUMBERS = [
        "359111222333",
        "1888111222",
        "+12312312312",
    ]

    def setUp(self) -> None:
        self.user = self._create_user_with_valid_values()

    def test__valid_name__expect_correct(self):
        for name in self.VALID_NAMES:
            with self.subTest(name=name):
                self.assertIsNone(name_validator(name))

    def test__invalid_name__expect_raise(self):
        for name in self.INVALID_NAMES:
            with self.subTest(name=name):
                with self.assertRaises(ValidationError):
                    name_validator(name)

    def test__valid_phone_number__expect_correct(self):
        for phone in self.VALID_PHONE_NUMBERS:
            with self.subTest(phone=phone):
                self.assertIsNone(phone_number_validator(phone))

    def test__invalid_phone_number__expect_raise(self):
        for phone in self.INVALID_PHONE_NUMBERS:
            with self.subTest(phone=phone):
                with self.assertRaises(ValidationError):
                    phone_number_validator(phone)
