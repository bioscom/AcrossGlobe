from django import forms
from django.contrib.auth.models import User
from .models import events

class EventForm(forms.ModelForm):
    class Meta:
         model = events
         fields = ('eventname', 'image', 'startdate', 'starttime', 'enddate', 'endtime', 'details', 'eventtype', 'category',)
         widgets = {
            'startdate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start date', 'class': 'form-control'}),
            'enddate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
            'starttime': forms.DateInput(attrs={'type': 'time', 'placeholder': 'Start time', 'class': 'form-control'}),
            'endtime': forms.DateInput(attrs={'type': 'time', 'placeholder': 'End time', 'class': 'form-control'}),
            'details': forms.Textarea(attrs={'rows':3, 'cols':10}),
            'eventtype': forms.Select(attrs={'placeholder': 'Is it on person or virtual?', 'class': 'form-control'}),
            'category': forms.Select(attrs={'placeholder': 'Event Category', 'class': 'form-control'}),
         }