from django.conf import settings
from django.conf.urls.static import static

from django.urls import path, include
from charity_app.accounts import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register-user'),
    path('login/', views.LoginUserView.as_view(), name='login-user'),
    path('logout/', views.LogoutUserView.as_view(), name='logout-user'),

    path('user/<int:pk>/', include([
        path('profile/', views.ProfileView.as_view(), name='profile-finish-user'),
        path('organization/', views.OrganizationView.as_view(), name='organization-finish-user'),

        path('profile/update/', views.ProfileUserView.as_view(), name='profile-user'),
        path('organization/update/', views.OrganizationUserView.as_view(), name='organization-user'),

        path('delete/', views.ProfileDeleteView.as_view(), name='delete-user'),
    ])),

    path('messages/', views.MessagesListView.as_view(), name='messages-superuser'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
