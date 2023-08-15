from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('charity_app.common.urls')),
    path('', include('charity_app.accounts.urls')),
    path('projects/', include('charity_app.projects.urls')),
    path('blog/', include('charity_app.blogs.urls')),
]
