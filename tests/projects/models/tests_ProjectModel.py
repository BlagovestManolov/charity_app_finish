from django.core.exceptions import ValidationError
from django.test import TestCase

from charity_app.projects.validators import project_name_validator


class ProjectTest(TestCase):
    def test__valid_project_name__expect_create(self):
        valid_names = [
            'Project Name',
            'Charity Project',
            'Another Test',
        ]

        for name in valid_names:
            with self.subTest(name=name):
                self.assertIsNone(project_name_validator(name))

    def test__invalid_project_name__expect_raise(self):
        invalid_names = [
            "123 Project",
            "Project_Name",
            "Test@Project"
        ]

        for name in invalid_names:
            with self.subTest(name=name):
                with self.assertRaises(ValidationError):
                    project_name_validator(name)
