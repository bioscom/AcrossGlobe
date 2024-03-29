from django import forms
from django.contrib.auth.models import User
from .models import Profile
#from phonenumber_field.formfields import PhoneNumberField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'image', )
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
            )
         }


class ProfileForm(forms.ModelForm):
    #phone_no = PhoneNumberField()
    class Meta:
         model = Profile
         fields = ('date_of_birth', 'gender', 'phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image',)
         widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows':3, 'cols':10}),
         }
         

class PasswordResetForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )