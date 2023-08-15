import re

from django.core.exceptions import ValidationError


def name_validator(value):
    pattern = r'[A-Z][a-z]+$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Name must start with an uppercase letter and '
            'contain only lowercase letters.'
        )


def organization_name_validator(value):
    pattern = r'\b[A-Z][a-zA-Z]*\b'

    if not re.match(pattern, value):
        raise ValidationError(
            'Organization name must start with an uppercase letter and '
            'contain only lowercase letters.'
        )


def phone_number_validator(value):
    pattern = r'^(\+359\d{9})$|^0\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid Bulgarian phone number. It must start'
            'with `+359` and have 13 digits or start with'
            '`0` and have 10 digits.'
        )
