from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib import messages
from .models import Service, Testimonial, ReviewInvitation, Appointment
from .forms import AppointmentForm, TestimonialForm
from django.utils import timezone

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
    testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')
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
            
            # Debug: Check email configuration
            print(f"Email configuration check:")
            print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
            print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
            print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
            print(f"EMAIL_HOST_PASSWORD: {'SET' if settings.EMAIL_HOST_PASSWORD else 'NOT SET'}")
            print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
            
            # Send to the business owner (with error handling)
            try:
                print(f"Attempting to send notification email to bailey@gardengalsofgeorgia.com")
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    ['bailey@gardengalsofgeorgia.com'],  # Owner's email
                    html_message=html_message,
                    fail_silently=True,  # Don't fail if email doesn't work
                )
                print(f"Notification email sent successfully")
            except Exception as e:
                # Log the error but don't break the form submission
                print(f"Failed to send notification email: {e}")
                print(f"Error type: {type(e).__name__}")
            
            # Send confirmation to the customer (with error handling)
            try:
                customer_subject = 'Your Callback Request - Garden Gals of Georgia'
                customer_html = render_to_string('core/email/callback_confirmation.html', {
                    'appointment': appointment,
                })
                customer_plain = strip_tags(customer_html)
                
                print(f"Attempting to send confirmation email to {appointment.email}")
                send_mail(
                    customer_subject,
                    customer_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [appointment.email],  # Customer's email
                    html_message=customer_html,
                    fail_silently=True,  # Don't fail if email doesn't work
                )
                print(f"Confirmation email sent successfully")
            except Exception as e:
                # Log the error but don't break the form submission
                print(f"Failed to send confirmation email: {e}")
                print(f"Error type: {type(e).__name__}")
            
            # Store appointment ID in session for success page
            request.session['last_appointment_id'] = appointment.id
            
            return redirect('appointment_success')
    else:
        form = AppointmentForm()
    
    return render(request, 'core/appointment.html', {'form': form})

def appointment_success(request):
    appointment_id = request.session.get('last_appointment_id')
    if appointment_id:
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            # Clear the session data
            if 'last_appointment_id' in request.session:
                del request.session['last_appointment_id']
            return render(request, 'core/appointment_success.html', {'appointment': appointment})
        except Appointment.DoesNotExist:
            pass
    
    # Fallback if no appointment found
    return render(request, 'core/appointment_success.html', {'appointment': None})

def privacy(request):
    return render(request, 'core/privacy.html')

def add_testimonial(request, token):
    invitation = get_object_or_404(ReviewInvitation, token=token)
    
    # Check if invitation is valid (not used)
    if invitation.is_used:
        messages.error(request, "This invitation link has expired or already been used.")
        return redirect('landing')
    
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.first_name = invitation.customer_name or invitation.customer_email
            testimonial.review_invitation = invitation
            testimonial.save()
            
            # Mark invitation as used
            invitation.is_used = True
            invitation.used_at = timezone.now()
            invitation.save()
            
            messages.success(request, "Thank you for your review! It will be displayed on our site after approval.")
            return redirect('landing')
    else:
        # Pre-fill the name from the invitation
        form = TestimonialForm(initial={'first_name': invitation.customer_name or invitation.customer_email})
    
    return render(request, 'core/add_testimonial.html', {
        'form': form,
        'invitation': invitation
    })
