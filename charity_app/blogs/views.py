from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, DeleteView

from charity_app.accounts.models import CharityUser
from charity_app.blogs.forms import BlogPostForm, CommentForm
from charity_app.blogs.models import Blogs, BlogComments
from charity_app.projects.models import Project


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = Blogs
    template_name = 'blogs/create-blog-page.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('blog-list')

    def get_form_kwargs(self):
        """To take only the projects accosted to the authenticated organization"""
        kwargs = super().get_form_kwargs()
        user_projects = Project.objects.filter(organization=self.request.user)
        kwargs['user_projects'] = user_projects
        return kwargs

    def form_valid(self, form):
        form.instance.project_id = self.request.POST.get('project')
        return super().form_valid(form)


class BlogsView(ListView):
    template_name = 'blogs/blog.html'
    model = Blogs
    context_object_name = 'blogs'
    paginate_by = 3
    ordering = ['-date_of_creation']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-date_of_creation')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = BlogComments
    form_class = CommentForm
    template_name = 'blogs/add-coment-page.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        blog_id = self.kwargs['blog_id']
        form.instance.blog_id = blog_id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog-list')


class CommentReadView(ListView):
    model = BlogComments
    template_name = 'blogs/read-comments.html'
    context_object_name = 'comments'

    def get_queryset(self):
        blog_id = self.kwargs['blog_id']
        return BlogComments.objects.filter(blog_id=blog_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_id = self.kwargs['blog_id']
        context['blog_information'] = Blogs.objects.get(pk=blog_id)
        return context


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogComments
    form_class = CommentForm
    template_name = 'blogs/add-coment-page.html'

    def get_success_url(self):
        return reverse_lazy('blog-list')


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogComments
    template_name = 'blogs/delete-comment-page.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('read-comment', kwargs={'blog_id': self.object.blog_id})
