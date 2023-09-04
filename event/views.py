from django.shortcuts import render
import requests
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
import folium
from folium import plugins

from geopy.geocoders import ArcGIS, Nominatim
import geopy

from .models import Place

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import *




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
    
    
# @login_required(login_url='/account/login')
# def add_event(request):
#     category = Categories.objects.all()
    
#     if request.method == "POST":
#         form = EventForm(data=request.POST, files=request.FILES)
#         if form.is_valid():    
#             e = form.save(commit=False)
#             e.author = request.user
#             e.save()
#             return redirect('event/events')
#     else:
#         form = EventForm()
        
#         ip = requests.get('https://api.ipify.org?format=json')
#         ip_data = json.loads(ip.text)
#         res = requests.get('http://ip-api.com/json/' + ip_data['ip'])
#         location_data = json.loads(res.text)
        
#         map = folium.Map(location=[location_data['lat'], location_data['lon']], zoom_start=8)
#         coordinates = (location_data['lat'], location_data['lon'])
#         icon=folium.Icon(color='red')
#         folium.Marker(coordinates, icon=icon).add_to(map)
#         plugins.Geocoder().add_to(map)
        
#     return render(request, "event/partial_create_event.html", {'form': form, 'category':category, 'map': map._repr_html_()})

@login_required(login_url='/account/login')
def add_event(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST, files=request.FILES)
        if form.is_valid():
            new_events = events(eventname = request.POST['eventname'], location = request.POST['location'], author = request.user,
                                image = request.POST['image'], startdate = request.POST['startdate'], starttime = request.POST['starttime'],
                                enddate = request.POST['enddate'], endtime = request.POST['endtime'],
                                details = request.POST['details'], eventtype = request.POST['eventtype'],
                                category = request.POST['category'], eventvenue = request.POST['eventvenue'],
                                virtual_type = request.POST['virtual_type'],
            )
            new_events.save()
            return redirect("event/events/")
    else:
        form = NewEntryForm()
    return render(request, "event/partial_create_event.html", {'form': form})


def event_detail(request, slug):
    categories = Categories.objects.all()
    mevent = events.objects.get(slug=slug)
    
    mday = mevent.startdate.strftime("%d").upper()
    eventdate = mevent.startdate.strftime("%A, %B %d,  %Y").upper()
    
    m = folium.Map(location=[mevent.latitudes, mevent.longitudes], zoom_start=9)
    # add a marker to the map
    coordinates = (mevent.latitudes, mevent.longitudes)
    icon=folium.Icon(color='red')
    folium.Marker(coordinates, popup=mevent.eventname, icon=icon).add_to(m)
    return render(request, 'event/detail.html', {'event': mevent, 'categories': categories, 'eventdate':eventdate, 'date':mday, 'map':m._repr_html_()})


def popup_map(request, slug):
    mevent = events.objects.get(slug=slug)
    m = folium.Map(location=[mevent.latitudes, mevent.longitudes], zoom_start=9)
    
    # add a marker to the map
    coordinates = (mevent.latitudes, mevent.longitudes)
    icon=folium.Icon(color='red')
    folium.Marker(coordinates, popup=mevent.eventname, icon=icon).add_to(m)
    
    return render(request, 'event/partial_popup_map.html', {'event': mevent, 'map':m._repr_html_()})
    

# Create your views here.
def index(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/'+ ip_data['ip'])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    return render(request, 'index.html', {'data': location_data})

        

@ajax_required
@login_required(login_url='/account/login')
@require_POST
def post_like(request):
    evt_id = request.POST.get('id')
    action = request.POST.get('action')
    if evt_id and action:
        try:
            evt = events.objects.get(id=evt_id)
            if action == 'like':
                evt.users_like.add(request.user)
            else:
                evt.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


# =================== React Modules =============================


@api_view(['GET', 'POST'])
def events_list0(request):
    if request.method == 'GET':
        data = events.objects.all()
        serializer = EventSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def event_detail0(request, pk):
    try:
        event = events.objects.get(pk=pk)
    except events.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    