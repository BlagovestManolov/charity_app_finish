from enum import Enum

from django.core.validators import MinLengthValidator
from django.db import models

from charity_app.accounts.mixins import ChoicesMixin
from charity_app.accounts.models import CharityUser
from charity_app.projects.validators import project_name_validator


class ProjectType(ChoicesMixin, Enum):
    Looking_For_Volunteers = 'LFV'
    Seeking_Financial_Aid = 'SFA'
    Seeking_Material_Aid = 'SMA'


class Project(models.Model):
    PROJECT_NAME_MAX_LEN = 255
    PROJECT_NAME_MIN_LEN = 8

    organization = models.ForeignKey(
        CharityUser,
        on_delete=models.CASCADE,
    )

    project_name = models.CharField(
        max_length=PROJECT_NAME_MAX_LEN,
        validators=(
            MinLengthValidator(PROJECT_NAME_MIN_LEN),
            project_name_validator,
        )
    )

    project_description = models.TextField()

    project_type = models.CharField(
        max_length=ProjectType.max_len(),
        choices=ProjectType.choices(),
    )

    is_active = models.BooleanField(
        default=True,
    )

    volunteers = models.ManyToManyField(
        CharityUser,
        related_name='project_volunteers',
    )

    date_of_creation = models.DateField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.project_name


class ProjectImages(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images',
    )

    image = models.ImageField(
        upload_to='project-images/',
        null=True,
        blank=True,
    )
