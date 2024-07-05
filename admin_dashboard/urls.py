from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve_driver/<int:driver_id>/', views.approve_driver, name='approve_driver'),
    path('approved_drivers/', views.driver_profile, name='approved_drivers'),
]
