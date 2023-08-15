from django.urls import path
from charity_app.common import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('get-involved/', views.GetInvolvedView.as_view(), name='get-involved'),

    path('love/', views.GiveLoveView.as_view(), name='give-love'),
    path('future/', views.GiveFutureView.as_view(), name='give-future'),
    path('education/', views.GiveEducationView.as_view(), name='give-education'),
    path('happiness/', views.GiveHappinessView.as_view(), name='give-happiness'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutView.as_view(), name='about'),

    path('become-a-volunteer/', views.VolunteerView.as_view(), name='become-volunteer'),
    path('happy-giving/', views.HappyGivingView.as_view(), name='happy-giving'),
    path('donation/', views.DonationView.as_view(), name='donation'),

    path('404/', views.custom_page_not_found, name='not-found')
]
