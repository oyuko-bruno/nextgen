# from django.urls import path
# from . import views

# urlpatterns = [
#     path('booking/', views.booking_page, name='booking'),
#     path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
#     path('confirm_booking/<int:selected_driver_id>/', views.confirm_booking, name='confirm_booking'),
#     path('booking//<int:driver_id>/', views.booking_page, name='booking'),
    
# ]
  

from django.urls import path
from .views import booking_page, select_driver_view,confirm_booking
from drivers.views import store_selected_driver

urlpatterns = [
    path('booking/', booking_page, name='booking'),
    path('booking/<int:driver_id>/',booking_page, name='booking'),
    path('select_driver/', select_driver_view, name='select_driver'),
    path('store_selected_driver/', store_selected_driver, name='store_selected_driver'),
    path('confirm_booking/<int:booking_id>/', confirm_booking, name='confirm_booking'),
]
