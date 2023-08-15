from django import forms
from django.core.validators import MinLengthValidator
from django.forms import formset_factory

from charity_app.projects.models import Project, ProjectType, ProjectImages
from charity_app.projects.validators import project_name_validator


class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name', 'project_description', 'project_type')


class SearchProjectForm(forms.Form):
    PROJECT_TYPE = [
        (None, 'All'),
        ('LFV', 'Volunteers'),
        ('SFA', 'Financial Aid'),
        ('SMA', 'Material Aid'),
    ]

    project_name = forms.CharField(
        label='Project Name',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter project name'
            }
        )
    )
    project_type = forms.ChoiceField(
        label='Project Type',
        required=False,
        choices=PROJECT_TYPE,
    )


class ImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImages
        fields = ('image',)


ImageFormSet = formset_factory(ImageForm, extra=3)
