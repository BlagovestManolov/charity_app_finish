from django.core.exceptions import ValidationError
from django.test import TestCase

from charity_app.accounts.validators import organization_name_validator
from tests.accounts.models.mixin import CreateProfileObjectsMixin


class OrganizationUserProfileTest(CreateProfileObjectsMixin, TestCase):
    VALID_ORGANIZATION_NAME = [
        'Test Organization',
        'Test Two',
        'Test Three',
    ]

    INVALID_ORGANIZATION_NAME = [
        'test 1organization',
        'test !',
        'test123',
    ]

    def test__valid_organization_name__expect_correct(self):
        for organization_name in self.VALID_ORGANIZATION_NAME:
            with self.subTest(organization_name=organization_name):
                self.assertIsNone(organization_name_validator(organization_name))

    def test__invalid_organization_name__expect_raise(self):
        for organization_name in self.INVALID_ORGANIZATION_NAME:
            with self.subTest(name=organization_name):
                with self.assertRaises(ValidationError):
                    organization_name_validator(organization_name)
