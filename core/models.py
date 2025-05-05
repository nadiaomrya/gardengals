from django.db import models

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True)  # Optional icon CSS class

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    first_name = models.CharField(max_length=30)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, f"{i} Stars") for i in range(1, 6)])
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} - {self.service}"

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
