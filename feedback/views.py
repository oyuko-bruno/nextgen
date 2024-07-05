from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from .forms import ContactForm
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Save to database
            contact_message = ContactMessage.objects.create(name=name, email=email, message=message)
            contact_message.save()
            # Send email notification
            send_mail(
                'New Contact Us Message',
                f'You have received a new message from {name} ({email}):\n\n{message}',
                'lindahkima@gmail.com',  
                ['email'],  
                fail_silently=False,
            )
    return render(request, 'base.html')
