from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime, timedelta

from .models import BookingFormData 

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        user = None

        # Check if input is an email
        if '@' in email_or_phone:
            user = User.objects.filter(email=email_or_phone).first()
        else:
            # Check if input is a phone number
            user = User.objects.filter(phone_number=email_or_phone).first()
        
        if user:
            user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('booking')  # Redirect to the intended page
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
            
    if is_booking_page_inactive(request.user):
        # Clear any existing form data
        clear_booking_form_data(request.user)
    else:
        # Restore form data from the database
        restore_booking_form_data(request.user)

    # Remove this line as it's not needed here
    # return render(request, 'login.html')

def is_booking_page_inactive(user):
    # Check if the user's last activity on the booking page is older than a certain period
    last_activity_time = user.last_activity_on_booking_page
    if last_activity_time:
        inactive_period = datetime.now() - last_activity_time
        return inactive_period > timedelta(minutes=30)  # Example: 30 minutes
    return True

def clear_booking_form_data(user):
    # Clear any existing form data associated with the user
    BookingFormData.objects.filter(user=user).delete()

def restore_booking_form_data(user):
    # Restore form data from the database
    form_data = BookingFormData.objects.filter(user=user).first()
    if form_data:
        # Set form data in session or render it in the template
        # ...
        pass

def save_booking_form_data(user, form_data):
    # Save form data in the database
    BookingFormData.objects.update_or_create(user=user, defaults={'form_data': form_data})

def signup_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
        
        if '@' in email_or_phone:
            # Check for duplicate email
            if User.objects.filter(email=email_or_phone).exists():
                error_message = 'User with this email already exists!'
                messages.error(request, error_message)
                return render(request, 'signup.html', {'error_message': error_message})
            else:
                user = User.objects.create_user(username=email_or_phone, email=email_or_phone, password=password)
        else:
            # Check for duplicate phone number
            if User.objects.filter(phone_number=email_or_phone).exists():
                error_message = 'User with this phone number already exists!'
                messages.error(request, error_message)
                return render(request, 'signup.html', {'error_message': error_message})
            else:
                user = User.objects.create_user(username=email_or_phone, phone_number=email_or_phone, password=password)
        
        login(request, user) 
        return redirect('login') 
    return render(request, 'signup.html')


