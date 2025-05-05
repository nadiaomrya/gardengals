from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from .models import Service, Testimonial, ReviewInvitation
from .forms import AppointmentForm, TestimonialForm

def landing(request):
    services = Service.objects.all()[:3]
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'core/landing.html', {
        'services': services,
        'testimonials': testimonials,
    })

def about(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'core/about.html', {'testimonials': testimonials})

def services(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})

def testimonials(request):
    testimonials = Testimonial.objects.filter(approved=True).order_by('-date')
    return render(request, 'core/testimonials.html', {'testimonials': testimonials})

def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            
            # Send email notification
            subject = 'New Callback Request from Garden Gals Website'
            html_message = render_to_string('core/email/callback_notification.html', {
                'appointment': appointment,
            })
            plain_message = strip_tags(html_message)
            
            # Send to the business owner
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                ['bailey@gardengalsofgeorgia.com'],  # Owner's email
                html_message=html_message,
                fail_silently=False,
            )
            
            # Send confirmation to the customer
            customer_subject = 'Your Callback Request - Garden Gals of Georgia'
            customer_html = render_to_string('core/email/callback_confirmation.html', {
                'appointment': appointment,
            })
            customer_plain = strip_tags(customer_html)
            
            send_mail(
                customer_subject,
                customer_plain,
                settings.DEFAULT_FROM_EMAIL,
                [appointment.email],  # Customer's email
                html_message=customer_html,
                fail_silently=False,
            )
            
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointment.html', {'form': form})

def privacy(request):
    return render(request, 'core/privacy.html')

def add_testimonial(request, token):
    invitation = get_object_or_404(ReviewInvitation, token=token)
    
    if not invitation.is_valid:
        messages.error(request, "This invitation link has expired or already been used.")
        return redirect('landing')
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.name = invitation.name
            testimonial.save()
            
            # Mark invitation as used
            invitation.used = True
            invitation.save()
            
            messages.success(request, "Thank you for your review! It will be displayed on our site after approval.")
            return redirect('landing')
    else:
        # Pre-fill the name from the invitation
        form = TestimonialForm(initial={'name': invitation.name})
    
    return render(request, 'core/add_testimonial.html', {
        'form': form,
        'invitation': invitation
    })
