import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from myblog.models import BlogPost
from .models import Profile
from .forms import LoginForm, PasswordResetForm, ProfileForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.models import User

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from .models import Contact
from django.core.mail import send_mail
from verify_email.email_handler import send_verification_email
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from user_visit.models import *
import datetime
from datetime import datetime
from smtplib import SMTPException


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username=cd['username']
            password=cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "You are successfully Logged In to Across Globe. For any area of improvement, kindly mail moderator under any of the sections below. Thanks for using AcrossGlobe.")
                    send_login_mail(request, user)
                    return redirect("/")
                else:
                    mymessage="You have not confirmed your email address yet. This means that you will not be able to reset your password if you lose it. "
                    mymessage=+"If you cannot find your confirmation email anymore, send yourself a new one " + f"<a href='#'> here.</a>"
                    messages.error(request, mymessage)
                    return redirect("/")
            else:
                messages.error(request, 'Invalid login!!! Username or password is incorrect. Check and try again later.')
                return redirect("/")
    else:
        form = LoginForm()
    return render(request, 'account/partial_login.html', {'form': form})
    # kindly refer to Login function in MyBlog:views.py line 452


def send_login_mail(request, user):
    obj = UserVisit.objects.filter(user_id=user.id).order_by('timestamp').last()
   
    subject = "Login Notification"
    datetime_obj = datetime.strptime(str(obj.timestamp),  "%Y-%m-%d %H:%M:%S.%f%z")
    
    source = ''
    if 'iPhone' in obj.ua_string:
        source = 'Mobile iPhone'
    elif 'Windows' in obj.ua_string:
        source = 'desktop'
    elif 'Android' in obj.ua_string:
        source = 'Mobile Android'
    
    message = "Dear user,\n \n"
    message += "You logged in at "+ str(datetime_obj.strftime('%I:%H %p')) + " on " + str(datetime.strptime(str(datetime_obj), "%Y-%m-%d %H:%M:%S.%f%z").date()) + " from the following "+ source +" device:\n"
    message += "User Agent: " + obj.ua_string + "\n"
    message += "IP Address: " + obj.remote_addr + "\n \n"
    message += "Best Regards, \n"
    message += "Across Globe, \n" 
    message += "https://acrossglobes.com/"
    
    try:
        sendermail = request.user.email
        receipientmail = [request.user.email]
        send_mail(subject, message, sendermail, receipientmail)
    except SMTPException as e:
         return JsonResponse({'status':'error'})
    return JsonResponse({'status':'ok'})
  

@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            new_user = form.save(commit=False) # Create a new user object but avoid saving it yet
            new_user.set_password(form.cleaned_data['password']) # Set the chosen password
            new_user.save() # Save the User object
            Profile.objects.create(user=new_user) # Create the user profile
            messages.success(request, 'You are successfully registered and an email has been sent to your email address, use the link in the e-mail to confirm your registration.')
        else:
            messages.error(request, 'Not sucessful, try again!')
            #return redirect("/")
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            #return redirect("/")
        else:
            messages.error(request, 'Error updating your profile')
            #return redirect("/")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile update was successful.")
            return redirect("/")
            #alert = True
            #return render(request, "account/partial_edit_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/partial_edit_profile.html", {'form': form})


# def edit_profile(request):
#     try:
#         profile = request.user.profile
#     except Profile.DoesNotExist:
#         profile = Profile(user=request.user, id=request.user.id)
#     if request.method == "POST":
#         form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             alert = True
#             return HttpResponse(status=204, headers={"postChanged": None, "showMessage": f"{request.user.author.first_name} updated."})
#             #return render(request, "account/partial_edit_profile.html", {'alert': alert})
#     else:
#         form = ProfileForm(instance=profile)
#     return render(request, "account/partial_edit_profile.html", {'form': form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'account/user/partial_list.html', {'section': 'people', 'users': users})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/partial_detail.html', {'section': 'people', 'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})


def user_profile(request, myid):
    object_list = BlogPost.objects.filter(author_id=myid).filter(parent_id__isnull=True).order_by('-dateTime')
    thisUser = User.objects.get(id=myid)
    
    # Paginate user's post list
    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post = paginator.page(paginator.num_pages)
    
    return render(request, "account/partial_user_profile.html", {'post': post, 'thisUser':thisUser})


def MyProfile(request, myid):
    object_list = BlogPost.objects.filter(author_id=myid).filter(parent_id__isnull=True).order_by('-dateTime')
    
    # Paginate user's post list
    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post = paginator.page(paginator.num_pages)
    
    return render(request, "account/partial_profile.html", {'post': post})





def password_change(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password sucessfuly changed")
            return redirect('/')
            #return render(request, "registration/password_reset_form.html", {'form': form})
            #return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"movieListChanged": None, "showMessage": f"{new_user.first_name} added." })})
    else:
        form = PasswordResetForm()
    return render(request, "registration/password_reset_form.html", {'form': form})


def Logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out. We expect to see you soon. Thanks for using AcrossGlobe.")
    return redirect('/')