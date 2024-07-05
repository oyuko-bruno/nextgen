from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

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
            # Check if the user is an admin
            if user.is_superuser:
                login(request, user)
                return redirect('admin:index')
            elif user.username == 'nextgen@io.com' and password == 'NextGen@20!':
                login(request, user)
                return redirect('admin_dashboard')  
            else:
                login(request, user)
                return redirect('booking')  
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
        
    return render(request, 'login.html')


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