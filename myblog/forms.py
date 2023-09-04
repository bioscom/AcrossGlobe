from django import forms
from django.urls import reverse_lazy
from .models import *  #Profile, BlogPost, BlogPostCategories, FileUploads, Comment, ReplyComment, CommentFileUploads, Advertisement
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from bootstrap_modal_forms.forms import BSModalModelForm
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostCategories
        fields = ('type', 'category_title', 'sub_title', 'moderatoremail', 'adrate', 'discount', 'discount_type', )
        widgets = {
            #     'type':forms.Select(TypeCategories),
            'category_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Category'}),
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostSubCategories
        fields = ('title', 'sub_title', 'moderatoremail', 'adrate', 'discount')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Sub Category'}),
        }

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    # image1 = forms.ImageField(label=_('File'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)
    # image2 = forms.ImageField(label=_('File'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)
    # image3 = forms.ImageField(label=_('File'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)
    # image4 = forms.ImageField(label=_('File'),required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = BlogPost
        # fields='__all__'
        fields = ('title', 'content', 'image1', 'image2', 'image3', 'image4',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the Blog'}),
        }
        labels = {
            'content': 'Message',
        }

class SubBlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = SubBlogPost
        # fields='__all__'
        fields = ('title', 'content', 'image1', 'image2', 'image3', 'image4',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the Blog'}),
            #"content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="comment"),
        }
        labels = {
            'content': 'Message',
        }
        

class EmailPostForm(forms.Form):
    #name = forms.CharField(max_length=25)
    #email = forms.EmailField()
    recepient_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    

class EmailModeratorForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(required=False, widget=forms.Textarea)
    
class ReportPostForm(forms.Form):
    message = forms.CharField(required=False, widget=forms.Textarea)


#  Lazy Users

class UserCreationForm(UserCreationFormBase):

    def get_credentials(self):
        return {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password1']}


