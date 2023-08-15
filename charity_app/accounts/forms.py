from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from charity_app.accounts.models import CharityUserProfile, OrganizationUserProfile

UserModel = get_user_model()


class RegisterUserForm(UserCreationForm):
    """
        Selecting certain fields to
        display when registering a new user.
    """
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'user_type', 'password1', 'password2')


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = CharityUserProfile
        fields = ('first_name', 'last_name', 'phone_number', 'profile_picture', 'information')


class OrganizationUserForm(forms.ModelForm):
    class Meta:
        model = OrganizationUserProfile
        fields = ('name', 'phone_number', 'information', 'profile_picture')
