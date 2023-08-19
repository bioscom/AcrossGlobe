from django.contrib.gis import forms
#from django import forms
from django.contrib.auth.models import User
from .models import Categories, events


class EventForm(forms.Form):
   #location = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500, 'zoom':9}))
   
   location = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 600, 'map_height': 400, 'default_lat': 50.1091, 'default_lon': 8.6819, 'default_zoom':9}))
   # class Meta:
   #    model = events
   fields = ('eventname', 'image', 'startdate', 'starttime', 'enddate', 'endtime', 'details', 'eventtype', 'category', 'eventvenue', 'virtual_type',)
   #location = forms.PointField()
   
   widgets = {
      'startdate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start date', 'class': 'form-control'}),
      'enddate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
      'starttime': forms.DateInput(attrs={'type': 'time', 'placeholder': 'Start time', 'class': 'form-control'}),
      'endtime': forms.DateInput(attrs={'type': 'time', 'placeholder': 'End time', 'class': 'form-control'}),
      'details': forms.Textarea(attrs={'rows':3, 'cols':10}),
      'eventtype': forms.Select(attrs={'placeholder': 'In person or virtual?', 'class': 'form-control'}),
      'virtual_type':forms.RadioSelect(choices=[(1, 'Zoom'), (2, 'Google Meet'), (3, 'Skype'), (4, 'TeamViewer'), (5, 'Free Conference Call')]),
   }
      
      

class EventFormR(forms.Form):
   category = forms.Select(attrs={'placeholder': 'Select Category', 'class': 'form-control'}),
   location = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 600, 'map_height': 400, 'default_lat': 50.1091, 'default_lon': 8.6819, 'default_zoom':9}))
   startdate = forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start date', 'class': 'form-control'}),
   enddate = forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
   starttime = forms.DateInput(attrs={'type': 'time', 'placeholder': 'Start time', 'class': 'form-control'}),
   endtime = forms.DateInput(attrs={'type': 'time', 'placeholder': 'End time', 'class': 'form-control'}),
   details = forms.Textarea(attrs={'rows':3, 'cols':10}),
   eventtype = forms.Select(attrs={'placeholder': 'In person or virtual?', 'class': 'form-control'}),
   virtual_type = forms.RadioSelect(choices=[(1, 'Zoom'), (2, 'Google Meet'), (3, 'Skype'), (4, 'TeamViewer'), (5, 'Free Conference Call')]),
   
   #fields = ('eventname', 'image', 'startdate', 'starttime', 'enddate', 'endtime', 'details', 'eventtype', 'category', 'longitude', 'latitude', 'eventvenue', 'virtual_type',)
   


class NewEntryForm(forms.Form):
   # ...
   location_name = forms.CharField(label='Name', max_length=20)
   location = forms.PointField(widget=forms.OSMWidget(attrs={ 'map_width': 600, 'map_height': 400, 'default_lat': 50.1091, 'default_lon': 8.6819, 'default_zoom': 9 }))
   
   startdate = forms.DateInput(attrs={'type': 'date', 'placeholder': 'Start date', 'class': 'form-control'}),
   enddate = forms.DateInput(attrs={'type': 'date', 'placeholder': 'End date', 'class': 'form-control'}),
   starttime = forms.DateInput(attrs={'type': 'time', 'placeholder': 'Start time', 'class': 'form-control'}),
   endtime = forms.DateInput(attrs={'type': 'time', 'placeholder': 'End time', 'class': 'form-control'}),
   details = forms.Textarea(attrs={'rows':3, 'cols':10}),
   eventtype = forms.Select(attrs={'placeholder': 'In person or virtual?', 'class': 'form-control'}),
   virtual_type =forms.RadioSelect(choices=[(1, 'Zoom'), (2, 'Google Meet'), (3, 'Skype'), (4, 'TeamViewer'), (5, 'Free Conference Call')]),