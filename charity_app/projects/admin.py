from django.contrib import admin

from charity_app.projects.models import Project, ProjectImages


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('organization_id', 'project_name', 'project_type', 'is_active', 'date_of_creation')
    list_filter = ('project_type', 'date_of_creation', 'is_active')
    ordering = ('organization_id',)


@admin.register(ProjectImages)
class ProjectImagesAdmin(admin.ModelAdmin):
    list_display = ('project', 'image')
    list_filter = ('project',)
