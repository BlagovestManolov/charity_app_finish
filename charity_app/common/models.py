from django.core.validators import MinLengthValidator
from django.db import models


class ContactUs(models.Model):
    NAME_MAX_LEN = 30
    NAME_MIN_LEN = 3

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=(
            MinLengthValidator(NAME_MIN_LEN),
        )
    )

    email = models.EmailField()

    message = models.TextField()

    date_time = models.DateTimeField(
        auto_now_add=True,
    )