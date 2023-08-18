import re

from django.core.exceptions import ValidationError


def name_validator(value):
    """
    Validate the format of a name.

    This function checks whether a given name follows a specific pattern:
        - Starts with an uppercase letter.
        - Contains only lowercase letters.
    """
    pattern = r'[A-Z][a-z]+$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Name must start with an uppercase letter and '
            'contain only lowercase letters.'
        )


def organization_name_validator(value):
    """
    Validate the format of an organization name.

    This function checks whether a given organization name follows a specific pattern:
        - Starts with an uppercase letter.
        - Contains only letters (both uppercase and lowercase).
    """
    pattern = r'\b[A-Z][a-zA-Z]*\b'

    if not re.match(pattern, value):
        raise ValidationError(
            'Organization name must start with an uppercase letter and '
            'contain only lowercase letters.'
        )


def phone_number_validator(value):
    """
    Validate the format of a Bulgarian phone number.

    This function checks whether a given phone number follows one of the specified patterns:
        - Starts with '+359' followed by 9 digits.
        - Starts with '0' followed by 9 digits.
    """
    pattern = r'^(\+359\d{9})$|^0\d{9}$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid Bulgarian phone number. It must start'
            'with `+359` and have 13 digits or start with'
            '`0` and have 10 digits.'
        )
