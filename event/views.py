from django.shortcuts import render
import json
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django import forms
from event.forms import *
from .models import Categories, events
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.utils.module_loading import import_string
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from datetime import timedelta

from hitcount.models import *
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin

from django.core.files.uploadedfile import SimpleUploadedFile
from itertools import chain
import datetime        #from datetime  Import datetime

# Create your views here.

def events_list(request):
    categories = Categories.objects.all() #.order_by('category_title')
    event_list = events.objects.filter().order_by('-datetime', 'category')
    
    paginator = Paginator(event_list, 33)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        mevents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        mevents = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        mevents = paginator.page(paginator.num_pages)
    return render(request, "event/index.html", {'events': mevents, 'categories': categories})


def event_list_by_category(request, cat_id):
    categories = Categories.objects.all()
    event_list = events.objects.filter(category_id=cat_id).order_by('-datetime', 'category')
    
    paginator = Paginator(event_list, 33)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        mevents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        mevents = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        mevents = paginator.page(paginator.num_pages)
    return render(request, "event/index.html", {'events': mevents, 'categories': categories})
    
@login_required(login_url='/account/login')
def add_event(request):
    try:
        #category = Categories.objects.get(id=cat_id)  
        if request.method == "POST":
            form = EventForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                e = form.save(commit=False)
                e.author = request.user
                e.save()
                return redirect('event/events')
        else:
            form = EventForm()
    except:
        pass
    return render(request, "event/partial_create_event.html", {'form': form})


def event_detail(request, id):
    mevent = events.objects.filter(id=id).first()
    return render(request, 'event/detail.html', {'event': mevent})

        

