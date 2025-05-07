from django import forms
from .models import Appointment, Testimonial

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'address', 'callback_time', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['first_name', 'rating', 'quote']
        widgets = {
            'quote': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Share your experience...'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Your first name'}),
        }
        labels = {
            'first_name': 'Your First Name',
            'rating': 'Your Rating (1-5 stars)',
            'quote': 'Your Review',
        } 