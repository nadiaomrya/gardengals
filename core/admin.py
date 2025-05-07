# pyright: reportMissingImports=false
# pyright: reportMissingModuleSource=false
from django.contrib import admin  # type: ignore
from django.urls import reverse
from django.utils.html import format_html
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Service, Testimonial, AppointmentRequest, ReviewInvitation

@admin.register(ReviewInvitation)
class ReviewInvitationAdmin(admin.ModelAdmin):
    list_display = ('customer_email', 'customer_name', 'is_sent', 'sent_at', 'is_used', 'used_at', 'created_at', 'testimonial_link')
    list_filter = ('is_sent', 'is_used', 'created_at', 'sent_at', 'used_at')
    search_fields = ('customer_email', 'customer_name', 'token')
    readonly_fields = ('token', 'sent_at', 'used_at', 'created_at', 'testimonial_link')
    actions = ['send_review_invitation_email']

    fieldsets = (
        (None, {
            'fields': ('customer_email', 'customer_name')
        }),
        ('Status (Read-only)', {
            'fields': ('token', 'is_sent', 'sent_at', 'is_used', 'used_at', 'testimonial_link'),
            'classes': ('collapse',), # Collapsible by default
        }),
    )

    def testimonial_link(self, obj):
        if hasattr(obj, 'testimonial_submission') and obj.testimonial_submission:
            testimonial = obj.testimonial_submission
            link = reverse("admin:core_testimonial_change", args=[testimonial.id])
            return format_html('<a href="{}">View Testimonial ({})</a>', link, "Approved" if testimonial.is_approved else "Pending")
        return "Not yet submitted"
    testimonial_link.short_description = 'Submitted Testimonial'

    def send_review_invitation_email(self, request, queryset):
        for invitation in queryset:
            if not invitation.is_sent and not invitation.is_used:
                # Construct the review submission link
                review_path = reverse('submit_review', kwargs={'token': str(invitation.token)})
                review_url = request.build_absolute_uri(review_path)

                context = {
                    'customer_name': invitation.customer_name or invitation.customer_email,
                    'review_url': review_url,
                    'site_name': 'Garden Gals of Georgia' # Or pull from settings/Site model
                }
                subject = f"Share Your Experience with {context['site_name']}"
                html_message = render_to_string('emails/review_invitation_email.html', context)
                plain_message = render_to_string('emails/review_invitation_email.txt', context)

                try:
                    send_mail(
                        subject,
                        plain_message,
                        settings.DEFAULT_FROM_EMAIL,
                        [invitation.customer_email],
                        html_message=html_message,
                        fail_silently=False,
                    )
                    invitation.mark_as_sent()
                    self.message_user(request, f"Invitation sent to {invitation.customer_email}.")
                except Exception as e:
                    self.message_user(request, f"Failed to send invitation to {invitation.customer_email}: {e}", level='ERROR')
            elif invitation.is_used:
                self.message_user(request, f"Invitation for {invitation.customer_email} has already been used.", level='WARNING')
            elif invitation.is_sent:
                self.message_user(request, f"Invitation for {invitation.customer_email} has already been sent.", level='WARNING')

    send_review_invitation_email.short_description = "Send selected invitations by email"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'rating', 'created_at', 'is_approved', 'review_invitation_link')
    list_filter = ('is_approved', 'rating', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('first_name', 'quote')
    readonly_fields = ('created_at', 'review_invitation_link')

    def review_invitation_link(self, obj):
        if obj.review_invitation:
            link = reverse("admin:core_reviewinvitation_change", args=[obj.review_invitation.id])
            return format_html('<a href="{}">{}</a>', link, obj.review_invitation)
        return "-"
    review_invitation_link.short_description = 'Review Invitation'
