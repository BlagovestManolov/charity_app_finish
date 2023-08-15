from django.test import TestCase
from django.urls import reverse

from tests.common.models.create_objects_mixin import CreateObjectsMixin
from charity_app.common.views import AboutView


class AboutTest(CreateObjectsMixin, TestCase):
    about = AboutView()

    def setUp(self) -> None:
        self.url = reverse('about')

    def test__response_code__expect_correct(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test__template_used__expect_correct(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'common/about.html')

    def test__context_data_with_valid_values__expect_correct(self):
        staff = self._create_user_with_is_staff_true()
        # Invalid staff
        not_staff = self._create_user_with_valid_values_two()

        response = self.client.get(reverse('about'))
        staffs = response.context['staffs']
        self.assertEqual(len(staffs), 1)
        self.assertIn(staff, staffs)
        self.assertNotIn(not_staff, staffs)
