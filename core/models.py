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
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

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
    email = models.EmailField()
    name = models.CharField(max_length=100)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Invitation for {self.name} ({self.email})"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiration to 30 days from creation by default
            self.expires_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)
    
    @property
    def is_valid(self):
        return not self.used and self.expires_at > timezone.now()
