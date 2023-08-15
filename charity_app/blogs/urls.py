from django.urls import path
from charity_app.blogs import views

urlpatterns = [
    path('', views.BlogsView.as_view(), name='blog-list'),
    path('add/', views.BlogPostCreateView.as_view(), name='add-blog'),
    path('create/comment/<int:blog_id>/', views.CommentCreateView.as_view(), name='add-comment'),
    path('read/comment/<int:blog_id>/', views.CommentReadView.as_view(), name='read-comment'),

    # Delete and Update comments
    path('update/comment/<int:pk>/', views.CommentUpdateView.as_view(), name='update-comment'),
    path('delete/comment/<int:pk>/', views.CommentDeleteView.as_view(), name='delete-comment'),
]