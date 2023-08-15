from django import forms
from django.test import TestCase
from charity_app.accounts.templatetags.custom_filters import placeholder, form_field_class


class CustomTemplateTagsTest(TestCase):
    def test__placeholder_tag__expect_correct(self):
        class TestForm(forms.Form):
            field = forms.CharField()

        form = TestForm()
        rendered_field = placeholder(form['field'], 'Enter your text')
        self.assertIn('placeholder="Enter your text"', str(rendered_field))

    def test__form_field_class_form__expect_correct(self):
        class TestForm(forms.Form):
            field = forms.CharField()

        form = TestForm()
        render_field = form_field_class(form['field'], 'custom-class')
        self.assertIn('class=" custom-class"', str(render_field))

