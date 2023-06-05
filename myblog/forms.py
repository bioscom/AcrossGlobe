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


CATEGORY_TYPES = [
    ('1', 'General'),
    ('2', 'Entertainment'),
    ('3', 'Science/Technology'),
]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostCategories
        fields = ('type', 'category_title', 'sub_title', 'moderatoremail', 'adrate', 'discount')
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
    class Meta:
        model = BlogPost
        # fields='__all__'
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the Blog'}),
            #"content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="comment"),
        }
        labels = {
            'content': 'Message',
        }

class SubBlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = SubBlogPost
        # fields='__all__'
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title of the Blog'}),
            #"content": CKEditor5Widget(attrs={"class": "django_ckeditor_5"}, config_name="comment"),
        }
        labels = {
            'content': 'Message',
        }


class FileUploadForm(forms.ModelForm):
    # file = ClearableFileInput(label='Message:')
    class Meta:
        model = FileUploads
        fields = ('file',)
        #widgets = ClearableFileInput(attrs={'allow_multiple_selected': True})
        widgets = {
            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
        }
        labels = {
            'file': '',
        }

class SubFileUploadForm(forms.ModelForm):
    # file = ClearableFileInput(label='Message:')
    class Meta:
        model = SubFileUploads
        fields = ('file',)
        #widgets = ClearableFileInput(attrs={'allow_multiple_selected': True})
        widgets = {
            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
        }
        labels = {
            'file': '',
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Message',
        }

class SubCommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = SubComment
        fields = ('content',)
        labels = {
            'content': 'Message',
        }
   

class Reply_CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Message',
        }


class Reply_SubCommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = SubComment
        fields = ('content',)
        labels = {
            'content': 'Message',
        }


class CommentFileUploadForm(forms.ModelForm):
    class Meta:
        model = CommentFileUploads
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
        }
        #widgets = ClearableFileInput(attrs={'allow_multiple_selected': True})
        
        labels = {
            'file': '',
        }

class SubCommentFileUploadForm(forms.ModelForm):
    class Meta:
        model = SubCommentFileUploads
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'allow_multiple_selected': True})
        }
        #widgets = ClearableFileInput(attrs={'allow_multiple_selected': True})
        
        labels = {
            'file': '',
        }

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    recepient_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    

class EmailModeratorForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(required=False, widget=forms.Textarea)


#  Lazy Users

class UserCreationForm(UserCreationFormBase):

    def get_credentials(self):
        return {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password1']}


class AdvertisementForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_action = reverse_lazy('advertisement')
    #     self.helper.form_method = 'GET'
    #     self.helper.add_input(Submit('submit', 'Submit'))
    
    
    expiration_date = forms.DateField(label='Start Date:', widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    #expiration_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}))
    class Meta:
        model = Advertisement
        fields = ('urllink', 'image', )
        labels = {
            'urllink': 'Landing Page',
        }