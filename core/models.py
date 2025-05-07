from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)  # Optional icon CSS class

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    first_name = models.CharField(max_length=100)
    quote = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, help_text="Admin must approve to display on site.")
    review_invitation = models.OneToOneField(
        'ReviewInvitation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='testimonial_submission'
    )

    def __str__(self):
        return f"Testimonial by {self.first_name} - {'Approved' if self.is_approved else 'Pending'}"

class Appointment(models.Model):
    CALLBACK_CHOICES = [
        ('morning', 'Morning (9am - 12pm)'),
        ('afternoon', 'Afternoon (12pm - 5pm)'),
        ('evening', 'Evening (5pm - 8pm)'),
        ('anytime', 'Anytime'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    callback_time = models.CharField(max_length=20, choices=CALLBACK_CHOICES, default='anytime')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.created_at.strftime('%Y-%m-%d')}"

class ReviewInvitation(models.Model):
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=200, blank=True, help_text="Optional, for personalizing the email.")
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_sent = models.BooleanField(default=False, help_text="Has the invitation email been sent?")
    sent_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False, help_text="Has this invitation been used to submit a review?")
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Used" if self.is_used else ("Sent" if self.is_sent else "Not Sent")
        return f"Invitation for {self.customer_email} ({status})"

    def mark_as_sent(self):
        self.is_sent = True
        self.sent_at = timezone.now()
        self.save()

    def mark_as_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()
