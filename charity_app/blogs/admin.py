from django.contrib import admin

from charity_app.blogs.models import Blogs, BlogComments


@admin.register(Blogs)
class BlogsAdmin(admin.ModelAdmin):
    list_display = ('project', 'blog_title', 'date_of_creation')
    list_filter = ('project', 'date_of_creation')


@admin.register(BlogComments)
class BlogCommentsAdmin(admin.ModelAdmin):
    list_display = ('blog', 'user', 'content', 'created_at')
    list_filter = ('blog', 'user', 'created_at')
