from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('porfolio', views.portfolio, name='portfolio'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contactResponse', views.contactResponse, name='contactResponse'),
    path('getProfiles', views.getProfiles, name="getProfiles"),
    path('profile/<str:pk>', views.single_portfolio, name="profile")
]

