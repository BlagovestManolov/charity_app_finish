from django.contrib import admin

from charity_app.common.models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'date_time')
    list_filter = ('date_time', 'email')

