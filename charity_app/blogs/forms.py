from django import forms

from charity_app.blogs.models import Blogs, BlogComments


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ('project', 'blog_title', 'blog_information')

    def __init__(self, *args, user_projects=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user_projects:
            self.fields['project'] = forms.ModelChoiceField(
                queryset=user_projects,
                label='Select a Project'
            )


class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComments
        fields = ['content']
