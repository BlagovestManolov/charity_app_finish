from django.contrib import admin

from charity_app.accounts.models import CharityUser, CharityUserProfile, OrganizationUserProfile


@admin.register(CharityUser)
class CharityUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'user_type', 'date_joined')
    list_filter = ('user_type', 'date_joined')
    ordering = ('id',)
    list_per_page = 10
    sortable_by = ('id', 'date_joined')


@admin.register(CharityUserProfile)
class CharityUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'phone_number')
    ordering = ('user_id', 'first_name')


@admin.register(OrganizationUserProfile)
class OrganizationUserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone_number')
    ordering = ('user_id',)
