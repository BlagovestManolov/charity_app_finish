import re

from django.core.exceptions import ValidationError


def project_name_validator(value):
    pattern = r'^[A-Za-z]+(?:\s+[A-Za-z]+)*$'

    if not re.match(pattern, value):
        raise ValidationError(
            'Project name must contain one or more words (only letters, no numbers, symbols, or whitespace).'
        )