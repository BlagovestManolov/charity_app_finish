from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView, RedirectView
from charity_app.accounts.forms import RegisterUserForm, ProfileUserForm, OrganizationUserForm
from charity_app.accounts.mixins import GetInformationFromModelMixin, GetCharityUserMixin, AddToContextMixin
from charity_app.accounts.models import CharityUserProfile, OrganizationUserProfile, CharityUser
from charity_app.common.models import ContactUs
from charity_app.projects.models import Project


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'user-account/register-user-page.html'
    success_url = reverse_lazy('login-user')


class LoginUserView(LoginView):
    template_name = 'user-account/login-user-page.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        if user.first_login:
            user.first_login = False
            user.save()

            if user.user_type == 'U':
                return redirect('profile-user', user.pk)
            else:
                return redirect('organization-user', user.pk)
        else:
            if user.user_type == 'U':
                return redirect('profile-finish-user', user.pk)
            else:
                return redirect('organization-finish-user', user.pk)


class LogoutUserView(LogoutView):
    pass


class ProfileUserView(UpdateView):
    template_name = 'user-account/update-information-user-page.html'
    model = CharityUserProfile
    form_class = ProfileUserForm

    def get_success_url(self):
        """
        Redirect to the finished profile
        user page.
        """
        user_pk = self.object.user.pk
        return reverse('profile-finish-user', kwargs={'pk': user_pk})


class OrganizationUserView(UpdateView):
    template_name = 'organization-account/organization-profile-update.html'
    model = OrganizationUserProfile
    form_class = OrganizationUserForm

    def get_success_url(self):
        """
        Redirect to the finished profile
        user page.
        """
        user_pk = self.object.user.pk
        return reverse('organization-finish-user', kwargs={'pk': user_pk})


class ProfileView(GetCharityUserMixin, GetInformationFromModelMixin, AddToContextMixin, DetailView):
    template_name = 'user-account/profile-user-page.html'
    model = CharityUserProfile

    def get_context_data(self, **kwargs):
        super().get_context_data(**kwargs)
        charity_user_profile = self._get_objects_from_model(CharityUserProfile, user=self._get_user()).first()

        context = self._add_to_context(
            charityuserprofile=charity_user_profile,
        )
        return context


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = CharityUser
    template_name = 'user-account/delete-user-page.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('index')


class OrganizationView(GetInformationFromModelMixin, GetCharityUserMixin, AddToContextMixin, DetailView):
    template_name = 'organization-account/organization-profile.html'
    model = OrganizationUserProfile

    def get_context_data(self, **kwargs):
        organization_user_profile = self._get_objects_from_model(OrganizationUserProfile, user=self._get_user()).first()
        active_projects = self._get_objects_from_model(
            Project,
            organization_id=self._get_user_primary_key(),
            is_active=True)
        inactive_projects = self._get_objects_from_model(
            Project,
            organization_id=self._get_user_primary_key(),
            is_active=False)

        context = self._add_to_context(
            organizationuserprofile=organization_user_profile,
            project_organization_active=active_projects,
            project_organization_no_active=inactive_projects,
        )
        return context


class MessagesListView(ListView):
    template_name = 'superuser/messages.html'
    model = ContactUs
    context_object_name = 'messages'
