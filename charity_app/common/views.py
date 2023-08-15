import random

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, CreateView
from charity_app.accounts.models import CharityUserProfile
from charity_app.blogs.models import Blogs
from charity_app.common.forms import ContactUsForm
from charity_app.common.mixin import TakeInformationForModelMixin, AddToContextMixin
from charity_app.common.models import ContactUs
from charity_app.projects.models import Project

UserModel = get_user_model()


class HomePageView(TakeInformationForModelMixin, AddToContextMixin, ListView):
    template_name = 'common/index.html'
    model = CharityUserProfile

    def get_context_data(self, *, object_list=None, **kwargs):
        random_users = self._get_n_random_objects_from_model(UserModel, 3, is_staff=False, user_type='U')
        random_projects = self._get_n_random_objects_from_model(Project, 3, is_active=True)
        random_blogs = self._get_n_random_objects_from_model(Blogs, 3)

        context = self._add_to_context(random_users=random_users,
                                       random_projects=random_projects,
                                       random_blogs=random_blogs)
        return context


class GetInvolvedView(TemplateView):
    template_name = 'common/get-inlovled.html'


class GiveEducationView(TemplateView):
    template_name = 'common/give-education-common-page.html'


class GiveFutureView(TemplateView):
    template_name = 'common/give-future-common-page.html'


class GiveLoveView(TemplateView):
    template_name = 'common/give-love-common-page.html'


class GiveHappinessView(TemplateView):
    template_name = 'common/give-happiness-common-page.html'


class ContactView(CreateView):
    template_name = 'common/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('index')
    model = ContactUs


class AboutView(TakeInformationForModelMixin, AddToContextMixin, ListView):
    template_name = 'common/about.html'
    model = UserModel

    def get_context_data(self, *, object_list=None, **kwargs):
        staff = self._get_objects_from_model(UserModel, is_staff=True)

        context = self._add_to_context(
            staffs=staff,
        )
        return context


class VolunteerView(TakeInformationForModelMixin, ListView):
    template_name = 'common/volunteer-page.html'
    model = Project
    paginate_by = 6
    context_object_name = 'projects'
    ordering = ['-date_of_creation']

    def get_queryset(self):
        """
            using your _get_objects_from_model method. Then, it applies
            `get_queryset` method first retrieves the filtered queryset
            the specified ordering using queryset.order_by(*self.ordering)
            to ensure that the ordering is consistent across
            all pages of the pagination.
        """
        queryset = self._get_objects_from_model(Project, project_type='LFV', is_active=True)
        queryset = queryset.order_by(*self.ordering)
        return queryset


class HappyGivingView(TakeInformationForModelMixin, ListView):
    template_name = 'common/happy-giving-page.html'
    model = Project
    paginate_by = 6
    context_object_name = 'projects'
    ordering = ['-date_of_creation']

    def get_queryset(self):
        """
            using your _get_objects_from_model method. Then, it applies
            `get_queryset` method first retrieves the filtered queryset
            the specified ordering using queryset.order_by(*self.ordering)
            to ensure that the ordering is consistent across
            all pages of the pagination.
        """
        queryset = self._get_objects_from_model(Project, project_type='SMA', is_active=True)
        queryset = queryset.order_by(*self.ordering)
        return queryset


class DonationView(TakeInformationForModelMixin, ListView):
    template_name = 'common/donation-page.html'
    model = Project
    paginate_by = 6
    context_object_name = 'projects'
    ordering = ['-date_of_creation']

    def get_queryset(self):
        """
            using your _get_objects_from_model method. Then, it applies
            `get_queryset` method first retrieves the filtered queryset
            the specified ordering using queryset.order_by(*self.ordering)
            to ensure that the ordering is consistent across
            all pages of the pagination.
        """
        queryset = self._get_objects_from_model(Project, project_type='SFA', is_active=True)
        queryset = queryset.order_by(*self.ordering)
        return queryset


def custom_page_not_found(request):
    return render(request, '404.html', status=404)
