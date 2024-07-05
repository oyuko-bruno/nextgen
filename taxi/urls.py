from django.urls import path
from . import views

urlpatterns = [
    path('', views.apply, name='apply'),
    path('application_success/<str:full_name>/', views.application_success, name='application_success'),
]


