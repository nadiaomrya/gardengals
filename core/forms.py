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
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us about your experience with Garden Gals...'}),
        } 