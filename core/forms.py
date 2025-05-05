from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'address', 'callback_time', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        } 