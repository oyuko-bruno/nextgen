from django.urls import path
from . import views

urlpatterns = [
    path('drivers/store_selected_driver/', views.store_selected_driver, name='store_selected_driver'),
]
