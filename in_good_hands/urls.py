"""in_good_hands URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from giveaway_app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.LandingPageView.as_view(), name='landing_page'),

    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditUserProfileView.as_view(), name='edit_profile'),
    path('profile/edit/password/', views.EditUserPasswordView.as_view(), name='change_password'),
    path('profile/taken-donation/<int:donation_id>/', views.DonationSetTakenView.as_view(), name='donation_status'),

    path('donate/', views.AddDonationView.as_view(), name='donate'),
    path('donate/confirmation', views.DonationConfirmationView.as_view(), name='form_confirmation'),
]
