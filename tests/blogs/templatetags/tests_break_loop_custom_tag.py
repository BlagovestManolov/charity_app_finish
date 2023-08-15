from django.template import Template, Context
from django.test import TestCase
from charity_app.blogs.templatetags.custom_filters_blog import break_loop


class CustomTemplateTagsTest(TestCase):
    def test__break_loop__expect_break(self):
        some_string = "{% load custom_filters_blog %} {{ text|break_loop:5 }}"
        template = Template(some_string)

        context = Context({'text': 'Blagovest'})

        render = template.render(context)
        self.assertEqual(render, ' Blago')
