# pyright: reportMissingImports=false
# pyright: reportMissingModuleSource=false
from django.contrib import admin  # type: ignore
from .models import Service, Testimonial, ReviewInvitation

@admin.register(ReviewInvitation)
class ReviewInvitationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'expires_at', 'used', 'is_valid')
    search_fields = ('name', 'email')
    readonly_fields = ('token',)
    list_filter = ('used',)
    
    actions = ['send_invitation_email']
    
    def send_invitation_email(self, request, queryset):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags
        from django.conf import settings
        
        for invitation in queryset:
            context = {
                'name': invitation.name,
                'review_url': f"https://gardengalsofgeorgia.com/testimonials/add/{invitation.token}/"
            }
            
            html_message = render_to_string('core/email/review_invitation.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                'We\'d Love Your Feedback - Garden Gals of Georgia',
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [invitation.email],
                html_message=html_message,
                fail_silently=False,
            )
        
        self.message_user(request, f"Sent {queryset.count()} invitation emails")
    
    send_invitation_email.short_description = "Send invitation email to selected customers"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'date', 'approved')
    list_filter = ('approved', 'rating')
    search_fields = ('name', 'text')
    actions = ['approve_testimonials']
    
    def approve_testimonials(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f"{queryset.count()} testimonials were approved.")
    
    approve_testimonials.short_description = "Approve selected testimonials"
