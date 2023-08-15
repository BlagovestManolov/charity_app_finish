from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, RedirectView, ListView, TemplateView, DetailView, FormView
from django.db.models import Q
from charity_app.projects.forms import AddProjectForm, SearchProjectForm, ImageFormSet
from charity_app.projects.models import Project, ProjectImages


# Create your views here.
class AddProject(LoginRequiredMixin, CreateView):
    form_class = AddProjectForm
    template_name = 'projects/new-project-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ImageFormSet(self.request.POST, self.request.FILES, prefix='images')
        else:
            context['formset'] = ImageFormSet(prefix='images')
        return context

    def form_valid(self, form):
        form.instance.organization = self.request.user
        formset = ImageFormSet(self.request.POST, self.request.FILES, prefix='images')
        if formset.is_valid():
            self.object = form.save()
            for form in formset:
                if 'image' in form.cleaned_data:
                    image = form.cleaned_data['image']
                    ProjectImages.objects.create(project=self.object, image=image)
            return redirect(self.get_success_url())

    def form_invalid(self, form):
        formset = ImageFormSet(self.request.POST, self.request.FILES, prefix='images')
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse_lazy('organization-finish-user', kwargs={'pk': self.object.organization_id})


class FinishProjectView(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        obj = Project.objects.get(pk=self.kwargs['pk'])
        obj.is_active = False
        obj.save()
        return reverse('organization-finish-user', kwargs={'pk': obj.organization_id})

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        return HttpResponseRedirect(url)


class ProjectsView(ListView):
    template_name = 'projects/projects-list.html'
    model = Project
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        form = SearchProjectForm(self.request.GET)

        if form.is_valid():
            project_name = form.cleaned_data.get('project_name')
            project_type = form.cleaned_data.get('project_type')

            if project_name and project_type:
                return Project.objects.filter(
                    Q(project_name__icontains=project_name) & Q(project_type__icontains=project_type) & Q(
                        is_active=True)
                )
            if project_name:
                return Project.objects.filter(
                    Q(project_name__icontains=project_name) & Q(is_active=True)
                )
            if project_type:
                return Project.objects.filter(
                    Q(project_type__icontains=project_type) & Q(is_active=True)
                )

            return Project.objects.filter(is_active=True).order_by('-id')
        return Project.objects.filter(is_active=True).order_by('-id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchProjectForm(self.request.GET)
        return context


class ProjectDetailsView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'projects/project-page.html'


class JoinProjectView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        project.volunteers.add(user)
        return redirect('project-detail', pk=project.pk)
