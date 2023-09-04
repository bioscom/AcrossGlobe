from django import forms
from django.urls import reverse_lazy
from .models import * 
from django.utils.translation import gettext_lazy as _

class AdminAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('urllink', 'is_approved',)
        widgets = {
            'urllink': forms.TextInput(),
        }
        labels = {
            'urllink': 'Landing Page',
        }

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('urllink', 'image', 'start_date', 'end_date', 'duration', )
        widgets = {
            'urllink': forms.TextInput(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            #'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd', 'class': 'form-control'}),
            'duration':forms.RadioSelect(choices=[(1, '1 Week'), (2, '2 Weeks'), (3, '3 Weeks'), (4, '4 Weeks')]),
        }
        labels = {
            'urllink': 'Landing Page',
        }
        
        
class PlaceAdvertForm(forms.ModelForm):
    class Meta:
        model = PlaceAdvert
        fields = ('category', 'adslot')
        

class PlaceAdvertSlotForm(forms.ModelForm):
    class Meta:
        model = PlaceAdvert
        fields = ()
        

class AdvertCreditForm(forms.ModelForm):
    class Meta:
        model = AdvertCredit
        fields=('credit',)