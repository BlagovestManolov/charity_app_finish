from enum import Enum
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse

from charity_app.accounts.mixins import ChoicesMixin
from charity_app.accounts.validators import name_validator, phone_number_validator, organization_name_validator


class UserType(ChoicesMixin, Enum):
    User = "U"
    Organization = "O"


class CharityUser(AbstractUser):
    # Delete fields from the user model
    first_name = None
    last_name = None

    email = models.EmailField(
        unique=True,
    )

    user_type = models.CharField(
        # max_length=UserType.max_len(),
        max_length=UserType.max_len(),
        choices=UserType.choices(),
        default=UserType.User.value,
    )

    first_login = models.BooleanField(
        default=True,
    )

    date_joined = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'{self.email}'


class CharityUserProfile(models.Model):
    FIRST_NAME_MAX_LEN = 30
    FIRST_NAME_MIN_LEN = 3
    LAST_NAME_MAX_LEN = 30
    LAST_NAME_MIN_LEN = 3
    PHONE_MAX_LEN = 13
    PHONE_MIN_LEN = 10
    INFORMATION_MAX_LEN = 300

    user = models.OneToOneField(
        CharityUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LEN),
            name_validator,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LEN),
            name_validator,
        )
    )

    phone_number = models.CharField(
        max_length=PHONE_MAX_LEN,
        validators=(
            MinLengthValidator(PHONE_MIN_LEN),
            phone_number_validator,
        )
    )

    profile_picture = models.ImageField(
        upload_to='user-photo/',
        blank=True,
        null=True,
    )

    information = models.TextField(
        max_length=INFORMATION_MAX_LEN,
    )


class OrganizationUserProfile(models.Model):
    NAME_MAX_LEN = 30
    NAME_MIN_LEN = 8
    PHONE_MAX_LEN = 13
    PHONE_MIN_LEN = 10
    INFORMATION_MAX_LEN = 300

    user = models.OneToOneField(
        CharityUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            MinLengthValidator(NAME_MIN_LEN),
            organization_name_validator,
        )
    )

    phone_number = models.CharField(
        max_length=PHONE_MAX_LEN,
        validators=(
            MinLengthValidator(PHONE_MIN_LEN),
            phone_number_validator,
        )
    )

    information = models.TextField(
        max_length=INFORMATION_MAX_LEN,
    )

    profile_picture = models.ImageField(
        upload_to='organization-photo/',
        blank=True,
        null=True,
    )