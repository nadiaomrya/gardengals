from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('appointment/', views.appointment, name='appointment'),
    path('privacy/', views.privacy, name='privacy'),
    path('testimonials/add/<uuid:token>/', views.add_testimonial, name='add_testimonial'),
] 