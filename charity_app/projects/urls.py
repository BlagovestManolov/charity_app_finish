from django.urls import path, include
from charity_app.projects import views

urlpatterns = [
    path('add/', views.AddProject.as_view(), name='add-project'),

    path('finish/<int:pk>/', views.FinishProjectView.as_view(), name='finish-project'),
    path('', views.ProjectsView.as_view(), name='projects-list'),

    path('<int:pk>/', views.ProjectDetailsView.as_view(), name='project-detail'),
    path('<int:pk>/join/', views.JoinProjectView.as_view(), name='project-join'),
]