from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        
        # Authenticate the user based on email/phone and password
        user = authenticate(request, username=email_or_phone, password=password)
        
        if user is not None:
            # If authentication succeeds, log in the user and redirect to booking page
            login(request, user)
            return redirect('booking')
        else:
            # If authentication fails, check if the email/phone exists in the database
            if '@' in email_or_phone:
                user_exists = User.objects.filter(email=email_or_phone).exists()
            else:
                user_exists = User.objects.filter(username=email_or_phone).exists()
            
            # Render the login page with appropriate error message
            if user_exists:
                # User exists but password is incorrect
                error_message = 'Password incorrect!'
            else:
                # User does not exist
                error_message = 'User not registered!'
                
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        email_or_phone = request.POST.get('email_or_phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            error_message = 'Passwords do not match.'
            return render(request, 'signup.html', {'error_message': error_message})
        
        user = None
        if '@' in email_or_phone:
            user = User.objects.filter(email=email_or_phone).first()
        else:
            user = User.objects.filter(username=email_or_phone).first()
        
        if user:
            # User already exists, authenticate and log them in
            user = authenticate(request, username=email_or_phone, password=password)
            if user is not None:
                login(request, user)
                return redirect('booking')
            else:
                error_message = 'Incorrect email or phone number!'
                messages.error(request, error_message)
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            # User does not exist, show error message
            error_message = 'User not registered!'
            messages.error(request, error_message)
            return render(request, 'signup.html', {'error_message': error_message})
    
    return render(request, 'signup.html')
