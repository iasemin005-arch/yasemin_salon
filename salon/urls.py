from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/services/', views.get_services_json, name='api_services'),
    path('api/masters/', views.get_masters_json, name='api_masters'),
    path('api/book/', views.book_appointment, name='book_appointment'),
    path('api/review/', views.submit_review, name='submit_review'),
]
