from django.urls import path
from . import views 

urlpatterns = [
    path('mpesa_stk_push/', views.mpesa_stk_push, name='mpesa_stk_push'),
    path('mpesa_confirmation/', views.mpesa_confirmation, name='mpesa_confirmation'),
    path('mpesa_validation/', views.mpesa_validation, name='mpesa_validation'),
]
