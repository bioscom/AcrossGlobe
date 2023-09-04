from django.shortcuts import render
import json
from django.shortcuts import get_object_or_404, render, redirect
from campaign.forms import *
from .models import *
from myblog.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hitcount.models import *
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from datetime import datetime, date, timedelta
from django.core.mail import send_mail, EmailMultiAlternatives
from smtplib import SMTPException
from django.http import JsonResponse
import datetime
from datetime import datetime
#import datetime

# Create your views here.

@login_required(login_url='/account/login')
def adverts(request, slug):
    category = get_object_or_404(BlogPostCategories, slug=slug)
    myadverts = get_object_or_404(Advertisement, user_id=request.user.id)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/en/' + slug + '/' + category.id + '/')
    else:
       form = AdvertisementForm()
    return render(request, 'campaign/partial_advertisement.html', {'form': form, 'category': category, 'myadverts': myadverts})


@login_required(login_url='/account/login')
def adverts(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST, files=request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.status = 'Pending'
            form.save()
            # Send a mail to Admin
            send_Advert_Request_mail(request)
            messages.success(request, "Your request for Advert has been successfully sent to Across Globe. Wait for an Admin to approve your request. For any area of improvement, kindly mail moderator under any of the sections. Thanks for using AcrossGlobe.")
            return redirect('/en/campaign/myads')
    else:
       form = AdvertisementForm()
    return render(request, 'campaign/partial_advertisement.html', {'form': form})

def send_Advert_Request_mail(request):   
    subject = "Advert Request Notification"
    
    message = "Dear Across Globe,\n \n"
    message += "Request to place advert on your website has been made by " + request.user.username  + " on " + str(now().date())
    message += "Best Regards, \n"
    message += "Across Globe, \n" 
    message += "https://www.acrossglobe.com/"
    
    try:
        sendermail = request.user.email
        receipientmail = [request.user.email]
        send_mail(subject, message, sendermail, receipientmail)
    except SMTPException as e:
         return JsonResponse({'status':'error'})
    return JsonResponse({'status':'ok'})



def edit_advertisement(request, pk):
    advert = Advertisement.objects.get(pk=pk)
    
    if request.method == "POST":
        if request.POST['start_date'] == '' or not 'duration' in request.POST:
            alert = True
            messages.error(request, "Either Start Date or Duration not selected. Select Start Date and Duration, and submit. Thanks for using Across Globe.")
            return redirect('/en/campaign/myads/')
        
        form = AdvertisementForm(request.POST, files=request.FILES, instance=advert)
        if form.is_valid():
            start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
            numofdays = int(request.POST['duration'])*7
            calcdate = (start_date + timedelta(days=numofdays))
            form.end_date = (start_date + timedelta(days=numofdays)) #Line to be dealt with!!!
            form.status = 'Pending'      
            form.save()
            return redirect('/en/campaign/myads/')
    else:
       form = AdvertisementForm(instance=advert)
    return render(request, 'campaign/partial_edit_advert.html', {'form': form})


def adrate(request):
    try:
        categories = BlogPostCategories.objects.all().order_by('category_title')
        subcategories = BlogPostSubCategories.objects.all()
        form = CategoryForm(data=request.POST, files=request.FILES)
        #return render(request, "blog/add_categories.html", {'form': form, 'categories': categories})
    except:
        pass
    return render(request, "campaign/adrate.html", {'form': form, 'categories': categories, 'subcategories': subcategories})


def available_ads_slots(request, pk):
    category = BlogPostCategories.objects.all()
    ads = PlaceAdvert.objects.filter(advert_id = None)
    selectedslot = request.POST.get("adslotradio")   # How to get the selected radio button.
    if selectedslot is not None:
        slot = PlaceAdvert.objects.get(id=selectedslot)
        form = PlaceAdvertSlotForm(request.POST, instance=slot)

    if request.method == 'POST':
        if form.is_valid():
            ad = form.save(commit=False)
            advert = Advertisement.objects.get(pk=pk)
            ad.advert = advert
            ad.save()
            advert.status = "Advertising"
            advert.save()
        return redirect('/en/campaign/myads/')
    else:
       form = PlaceAdvertForm()
    return render(request, 'campaign/partial_available_ads_slots.html', {'form': form, 'category': category, 'ads':ads})
    

def campaign(request):
    category = BlogPostCategories.objects.all().order_by('category_title')
   
    form = PlaceAdvertForm(request.POST)
    for cat in category:
        i = 1
        if not PlaceAdvert.objects.filter(category_id = cat.id).exists():
            advert = form.save(commit=False)
            while i <= 6 :
                advert.pk = None
                advert.category = cat
                advert.adslot = i
                advert.save()
                i += 1
    
    ads = PlaceAdvert.objects.all().order_by('category')
    return render(request, 'campaign/advert_slots.html', {'form': form, 'category': category, 'ads':ads})

def myads(request):
     myadverts = Advertisement.objects.filter(user_id = request.user.id)
     return render(request, 'campaign/myads.html', {'myadverts': myadverts})
 

#region =================  Admin ================
def allads(request):
     alladverts = Advertisement.objects.all().order_by('-creation_date')
     return render(request, 'campaign/admin_all_campaigns.html', {'alladverts': alladverts})
 
 
def approval(request, pk):
    ad = Advertisement.objects.get(pk = pk)
    form = AdminAdvertisementForm(request.POST, instance=ad)
    if request.method == "POST":
        if form.is_valid():
            advert = form.save(commit=False)
            if advert.is_approved == True:
                advert.status = 'Approved'
            else:
                advert.status = 'Denied'
            advert.save()
            
            #send mail to advert requestor
            send_Advert_Review_mail(request, ad)
            return redirect('/en/campaign/all_ads/')
    else:
       form = AdminAdvertisementForm(instance=ad)
    return render(request, 'campaign/admin_partial_approval.html', {'form': form})

def send_Advert_Review_mail(request, ad):   
    subject = "Advert Request Review Notification - Across Globe"
    
    text_content=""
    
    html_content = "<p>Dear " + ad.user.username + ", </p>"
    html_content += "Your request to place advert on across globe has been reviewed by " + request.user.username  + ", our administrator on " + str(now().date()) + ", "+ str(now().time())
    html_content += "<p>Click <a href='https://www.acrossglobe.com/en/campaign/myads/'>here</a> to view the review. </p>"
    
    html_content += "<p>If approved, on the list of your advert page, click on Edit botton to enter the advert start date, and select the duration to run the ad. </p>"
    html_content += "<p>Then click Advert button to publish the ad.</p>" 
    html_content += "<p>From the popup page, select the Ad Section where you want the ad to appear under any of the Ad sections.</p>"
    html_content += "<p>Then click Submit button.</p>"
    
    html_content += "<p>Best Regards, </p>"
    html_content += "<p><a href='https://www.acrossglobe.com/en/'>Across Globe</a></p>"
    
    try:
        sendermail = request.user.email
        receipientmail = [ad.user.email]
        msg = EmailMultiAlternatives(subject, text_content, sendermail, receipientmail)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #send_mail(subject, message, sendermail, receipientmail)
    except SMTPException as e:
         return JsonResponse({'status':'error'})
    return JsonResponse({'status':'ok'})


def advertcredit(request):
     credit = AdvertCredit.objects.filter()
     return render(request, 'campaign/admin_advertcredit_list.html', {'advertcredits': credit})
 
def addcredit(request):
    form = AdvertCreditForm(request.POST)
    users = User.objects.all()
    oUser = request.POST.get("username")
    if request.method == "POST":
        if form.is_valid():
            # Add new user credit
            credit = form.save(commit=False)
            credit.user = User.objects.get(pk=oUser)
            credit.modified_date = now()
            credit.save()
            return redirect('/en/campaign/advertcredit/')
    else:
        form = AdvertCreditForm()
    return render(request, 'campaign/partial_add_advert_credit.html', {'form':form, 'allusers':users})


def updatecredit(request, pk):
    users = User.objects.all()
    ad = AdvertCredit.objects.get(pk = pk)
    form = AdvertCreditForm(request.POST, instance=ad)
    #oUser = request.POST.get("username")
    if request.method == "POST":
        if form.is_valid():
            #update user credit
            #form.user = users
            form.modified_date = now()
            form.save()
            return redirect('/en/campaign/advertcredit/')
    else:
        form = AdvertCreditForm(instance=ad)
    return render(request, 'campaign/partial_add_advert_credit.html', {'form':form, 'allusers':users})
#endregion ======================================