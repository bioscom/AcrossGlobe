import json
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username=cd['username']
            password=cd['password']
            user = authenticate(request, username=username, password=password)
            #user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return redirect("/")
                else:
                    #messages.error(request, 'Disabled Account.')
                    return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"Disabled Account." })})
            else:
                # messages.error(request, 'Invalid login.')
                # return HttpResponse('Invalid login')
                return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"Invalid login. Try using the correct username and password" })})
    else:
        form = LoginForm()
    return render(request, 'account/partial_login.html', {'form': form})
    # kindly refer to Login function in MyBlog:views.py line 452


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return HttpResponse(status=200, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{new_user.first_name} added." })})
        else:
            return HttpResponse(status=200, headers={'HX-Trigger': json.dumps({"postChanged": None})}) # Means no content
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
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user, id=request.user.author_id)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "account/partial_edit_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/partial_edit_profile.html", {'form': form})


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
    post = BlogPost.objects.filter(author_id=myid).order_by('-dateTime')
    return render(request, "account/partial_user_profile.html", {'post': post})


def MyProfile(request, myid):
    post = BlogPost.objects.filter(author_id=myid).order_by('-dateTime')
    return render(request, "account/partial_profile.html", {'post': post})


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user, id=request.user.author_id)
    if request.method == "POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return HttpResponse(status=204, headers={"postChanged": None, "showMessage": f"{request.user.author.first_name} updated."})
            #return render(request, "account/partial_edit_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "account/partial_edit_profile.html", {'form': form})


# def password_change(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, "registration/password_reset_form.html", {'form': form})
#             #return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"movieListChanged": None, "showMessage": f"{new_user.first_name} added." })})
#     else:
#         form = PasswordResetForm()
#     return render(request, "registration/password_reset_form.html", {'form': form})


def Logout(request):
     messages.success(request, "Successfully logged out")
     logout(request)
     return redirect('/')