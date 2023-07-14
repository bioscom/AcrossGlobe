import json
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from django.contrib.auth.models import User
from django import forms
from myblog.forms import *
from .models import *
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

# from django.shortcuts import render
# from rest_framework.views import APIView
# from . serializer import *
# from rest_framework.response import Response

#region =============== Testing React Framework ===============================

# class ReactView(APIView):
#     def get(self, request):
#         output = [{"employee": output.employee,
                   
#                    }
#                   for output in BlogPost.objects.all()]
#         return Response(output)
    
#     def post(self, request):
#         serializers = ReactSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True)
        


#endregion ====================================================================




class AllKeywordsView(ListView):
    model = BlogPost
    template_name = "blog/blog.html"

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def category_by_type(request, pk):
    try:
        type = TypeCategories.objects.get(pk=pk)
        categories = BlogPostCategories.objects.filter(type_id=type.id)
        posts = BlogPost.objects.filter()
        
        # for cat in categories:
        #     if cat.id == topics.category_id:
        #         topics.count()
        
        
        #BlogPost.objects.filter(parent=post)
        #subcategories = BlogPostSubCategories.objects.all()
        #form = CategoryForm(data=request.POST, files=request.FILES)
        #return render(request, "blog/add_categories.html", {'form': form, 'categories': categories})
    except:
        pass
    return render(request, "blog/blog_types.html", {'type': type, 'categories':categories, 'posts':posts})


#region =============== Category ========================================================================================
def category_list(request):
    try:
        categories = BlogPostCategories.objects.all().order_by('type')
        subcategories = BlogPostSubCategories.objects.all()
        form = CategoryForm(data=request.POST, files=request.FILES)
        #return render(request, "blog/add_categories.html", {'form': form, 'categories': categories})
    except:
        pass
    return render(request, "blog/categories_list.html", {'form': form, 'categories': categories, 'subcategories': subcategories})

def add_category(request):
    try:
        categories = BlogPostCategories.objects.all()
        if request.method == "POST":
            form = CategoryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                category = form.save(commit=False)
                type_id = request.POST.get('type')
                category.type_id = type_id
                category.save()
                obj = form.instance
                alert = True
                return redirect('/en/category_list/')
                #return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"categoryListChanged": None, "showMessage": f"{category.category_title} added."})})
        else:
            form = CategoryForm()
    except:
        pass
    return render(request, "blog/partial_add_category.html", {'form': form, 'categories': categories})

def edit_category(request, pk):
    try:
        category = get_object_or_404(BlogPostCategories, pk=pk)
        #category = BlogPostCategories.objects.get(id=cat_id)
        if request.method == "POST":
            form = CategoryForm(data=request.POST, instance=category)
            if form.is_valid():
                form.save()
                #obj = form.instance
                #alert = True
                return redirect('/en/category_list/')
                #return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"categoryListChanged": None, "showMessage": f"{category.category_title} updated."})})
        else:
            form = CategoryForm(instance=category)
    except:
        pass
    return render(request, "blog/partial_edit_category.html", {'form': form, 'category': category})

#endregion

#region =============== List blog posts, List blog posts by category and blog details ===============================

def blogs_list(request):
    types = TypeCategories.objects.all()
    categories = BlogPostCategories.objects.all() #.order_by('category_title')
    categories = BlogPostCategories.objects.filter() #.order_by('category_title')
    object_list = BlogPost.objects.filter(is_approved=True).filter(parent_id__isnull=True).order_by('-dateTime', 'category')
    
    #most_recent = BlogPost.objects.order_by('-timestamp')[:3]
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    hits = HitCount.objects.all().filter(modified__gte=now()-timedelta(minutes=5))
    total_hit_count = 0
    for i in hits:
        total_hit_count += i.hits
        
    guest_users = total_hit_count if total_hit_count == 1 else abs(total_hit_count - active_users)
    
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(object_list, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_list.html", {'posts': posts, 'types': types, 'categories': categories, 'active_users':active_users, 'guest_users':guest_users})


def news_list(request):
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    types = TypeCategories.objects.all()
    categories = BlogPostCategories.objects.all() #.order_by('category_title')
    categories = BlogPostCategories.objects.filter() #.order_by('category_title')
    object_list1 = BlogPost.objects.filter().filter(parent_id__isnull=True).order_by('-dateTime', 'category')
    object_list2 = SubBlogPost.objects.filter().filter(parent_id__isnull=True).order_by('-dateTime', 'subcategory')
    
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(object_list1, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/news_list.html", {'posts': posts, 'types': types, 'categories': categories, 'active_users':active_users})


def blogByCategory(request, slug, cat_id):
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    category = BlogPostCategories.objects.filter(slug=slug).first()
    cattype = TypeCategories.objects.get(id=category.type_id)
    subcategories = BlogPostSubCategories.objects.all()
    object_list = BlogPost.objects.all()
    object_list = BlogPost.objects.filter(category=cat_id).filter(parent_id__isnull=True).order_by('-dateTime')
    
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(object_list, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_category.html", {'posts': posts, 'category': category, 'subcategories': subcategories, 'active_users':active_users, 'cattype':cattype })


def blogBySubCategory(request, slug):
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    subcategory = BlogPostSubCategories.objects.get(slug=slug)
    category = BlogPostCategories.objects.get(id=subcategory.category_id)
    
    object_list = SubBlogPost.objects.all()
    object_list = SubBlogPost.objects.filter(subcategory=subcategory.id).filter(parent_id__isnull=True).order_by('-dateTime')
    
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(object_list, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_sub_category.html", {'posts': posts, 'category': category, 'subcategories': subcategory, 'active_users':active_users })


def blog_details(request, slug): 
    post = BlogPost.objects.filter(slug=slug).first()
    
    post_viewed(request=request, slug=slug) # To know how many authenticated users viewed the post.
    if post is not None:
        hitcounter_view(request, post.pk, BlogPost) # To know how many authenticated and anonymous users viewed the post.
    
    if post is not None:
        category = BlogPostCategories.objects.filter(id=post.category_id).first()
        cattype = TypeCategories.objects.get(id=category.type_id)
        
    queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    datas = get_object_or_404(queryset, slug=slug)
    popular_posts = BlogPost.objects.filter(category_id=post.category_id).filter(parent_id__isnull=True).order_by('-hit_count_generic__hits')[:3]
    least_popular_posts = BlogPost.objects.filter(category_id=post.category_id).filter(parent_id__isnull=True).order_by('hit_count_generic__hits')[:3]
    
    hits = HitCount.objects.filter(object_pk = post.pk).first()
    guest_user = int(hits.hits) - datas.viewers.count()
    
    #object_list = BlogPost.objects.filter(parent_id=post.id).order_by('dateTime') #TODO; pay attention to this place
    # Paginate blog details
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(post.children, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_details.html", {'posts': post, 'comments':comments, 'datas': datas, 'category': category, 
                                                      'popular_posts': popular_posts, 'least_popular_posts': least_popular_posts, 
                                                      'guest_user':guest_user, 'cattype':cattype})


def blog_sub_details(request, slug): 
    post = SubBlogPost.objects.filter(slug=slug).first()
    
    # To know how many authenticated users and anonymous users that viewed the post.
    sub_post_viewed(request=request, slug=slug) 
    hitcounter_view(request, post.pk, SubBlogPost)
    if post is not None:
       
        subcategory = BlogPostSubCategories.objects.get(id=post.subcategory_id)
        category = BlogPostCategories.objects.get(id=subcategory.category_id)
        cattype = TypeCategories.objects.get(id=category.type_id)
        
    queryset = SubBlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    datas = get_object_or_404(queryset, slug=slug)
    popular_posts = SubBlogPost.objects.filter(subcategory_id=post.subcategory_id).filter(parent_id__isnull=True).order_by('-hit_count_generic__hits')[:3]
    least_popular_posts = SubBlogPost.objects.filter(subcategory_id=post.subcategory_id).filter(parent_id__isnull=True).order_by('hit_count_generic__hits')[:3]
    
    hits = HitCount.objects.filter(object_pk = post.pk).first()
    guest_user = int(hits.hits) - datas.viewers.count()
    
    #object_list = SubBlogPost.objects.filter(parent=post).order_by('dateTime') #TODO; pay attention to this place
        
    # Paginate blog details
    no_of_pages = Paginating.objects.get()
    paginator = Paginator(post.children, no_of_pages.number_of_pages)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)
        # 
    return render(request, "blog/blog_Sub_details.html", {'posts': post, 'comments': comments, 'datas': datas, 'category': category, 'subcategory':subcategory, 
                                                          'popular_posts': popular_posts, 'least_popular_posts': least_popular_posts, 'guest_user':guest_user, 'cattype':cattype})


def hitcounter_view(request, pk, dModel):
    object = get_object_or_404(dModel, pk=pk)
    context = {}

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(object)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    # … extra logic …
    return JsonResponse({'status': 'ok'})

#endregion

#region =============== Add New Post(new topic), Update and Delete post =================================================

@login_required(login_url='/account/login')
def add_post(request, cat_id):
    try:
        category = BlogPostCategories.objects.get(id=cat_id)  
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, files=request.FILES)
            
            if form.is_valid():
                blogpost = form.save(commit=False)
                blogpost.author = request.user
                blogpost.category = category
                blogpost.save()
                
                return redirect('/en/'+ blogpost.slug + '/')
        else:
            form = BlogPostForm()
    except:
        pass
    return render(request, "blog/partial_add_post.html", {'form': form, 'category': category})

def update_post(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        category = BlogPostCategories.objects.get(id=post.category_id)
        queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)
        
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, instance=post, files=request.FILES)
            if form.is_valid():
                post = form.save()
                return redirect('/en/'+ post.slug + '/#'+ str(post.pk))
        else:
            form = BlogPostForm(instance=post)
    except:
        pass
    return render(request, "blog/partial_edit_post.html", { 'form': form, 'post':post, 'category': category })

@login_required(login_url='/account/login')
def add_comment(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        category = BlogPostCategories.objects.get(id=post.category_id)
        if request.method == "POST":
            form = BlogPostForm(request.POST, files=request.FILES)
            if form.is_valid():
                blogpost = form.save(commit=False)
                #blogpost.title = post.title
                blogpost.author = request.user
                blogpost.category = category
                blogpost.parent = post
                blogpost.save()
                
                object_list = BlogPost.objects.filter(parent_id=post.id)
                no_of_pages = Paginating.objects.get()
                paginator = Paginator(object_list, no_of_pages.number_of_pages)
            
                return redirect('/en/'+ post.slug + '/?page=' + str(paginator.num_pages) + '#' + str(blogpost.id)) #/?page=2
        else:
            post.content = ''
            post.image1.name = ''
            post.image2.name = ''
            post.image3.name = ''
            post.image4.name = ''
            form = BlogPostForm(instance=post)
    except:
        pass
    return render(request, 'blog/partial_add_comment.html', {'form': form, 'posts': post, 'category': category})

def update_comment(request, id):
    try:
        post = BlogPost.objects.get(id=id)
        if post.parent_id is not None:
            parentpost = BlogPost.objects.get(id=post.parent_id)
            
        category = BlogPostCategories.objects.get(id=post.category_id)
        queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        #datas = get_object_or_404(queryset, slug=slug)
        
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, instance=post, files=request.FILES)
            if form.is_valid():
                post = form.save()
                if post.parent_id is not None:
                    return redirect('/en/'+ parentpost.slug + '/#'+ str(id))  #/?page=2
                else:
                    return redirect('/en/'+ post.slug + '/#'+ str(id))  #/?page=2
        else:
            form = BlogPostForm(instance=post)
    except:
        pass
    return render(request, "blog/partial_edit_comment.html", { 'form': form, 'post':post, 'category': category })

@login_required(login_url='/account/login')
def reply_post(request, id):
    post = BlogPost.objects.get(id=id)
    if post.parent_id is not None:
        parentpost = BlogPost.objects.get(id=post.parent_id)
        
    category = BlogPostCategories.objects.get(id=post.category_id)
    
    if request.method == "POST":
        form = BlogPostForm(request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.title = post.title
            blogpost.category = category
            blogpost.author = request.user
            if post.parent_id is not None:
                blogpost.parent = parentpost
            else:
                blogpost.parent = post
            blogpost.save()
            
            object_list = BlogPost.objects.filter(parent_id=post.id)
            no_of_pages = Paginating.objects.get()
            paginator = Paginator(object_list, no_of_pages.number_of_pages)
            
            if post.parent_id is not None:
                return redirect('/en/'+ parentpost.slug + '/?page=' + str(paginator.num_pages) + '#' + str(blogpost.id)) #/?page=2
            else:
                return redirect('/en/'+ post.slug + '/?page=' + str(paginator.num_pages) + '#' + str(blogpost.id)) #/?page=2
    else:
        if post.parent_id is not None:
            p = '<blockquote>' + '<p><a href=/' + parentpost.slug + '/#' + str(id) + '><b>' + post.author.username + ':</b></a></p>' + post.content.replace() + '</blockquote><p></p>'
        else:
            p = '<blockquote>' + '<p><a href=/' + post.slug + '/#' + str(id) + '><b>' + post.author.username + ':</b></a></p>' + post.content + '</blockquote><p></p>'

        post.content = p
        post.image1.name = ''
        post.image2.name = ''
        post.image3.name = ''
        post.image4.name = ''
        form = BlogPostForm(instance=post)
        
    return render(request, 'blog/partial_reply_post.html', {'form': form, 'post': post, 'category': category})

def Delete_Post(request, slug):
    post = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        if request.user == post.author:
            if check_if_less_than_seven_days(post.dateTime):
                post.delete()
                messages.success(request, '<b>'+ post.title + '</b> successfully deleted.')
                return redirect('/')
            else:
                messages.error(request, '<b>'+ post.title + '</b> can not be deleted, post more that 7 days.')
                return redirect('/' + slug + '/')
    return render(request, 'blog/delete_blog_post.html', {'posts': post})


def check_if_less_than_seven_days(postdate):
    d = datetime.datetime.strptime(str(postdate.date()), "%Y-%m-%d") # Add .date() if hour doesn't matter
    now = datetime.datetime.now()                 # Add .date() if hour doesn't matter
    return (now - d).days < 7

#endregion

#region =============== Add New SubPost(sub topic), Update and Delete sub post =================================================

@login_required(login_url='/account/login')
def add_sub_post(request, subcat_id):
    try:
        subcategory = BlogPostSubCategories.objects.get(id=subcat_id) 
        category = BlogPostCategories.objects.get(id=subcategory.category_id)  
        if request.method == "POST":
            form = SubBlogPostForm(data=request.POST, files=request.FILES)
            
            if form.is_valid():
                blogpost = form.save(commit=False)
                blogpost.author = request.user
                blogpost.subcategory = subcategory
                blogpost.save()
                
                return redirect('/en/'+ blogpost.slug +'/sub/')
                
                ################ Future Research work
                # When the submit button is pressed, the popup should disappear and refresh the main 
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
        else:
            form = SubBlogPostForm()
    except:
        pass
    return render(request, "blog/partial_add_sub_post.html", {'form': form, 'category': category, 'subcategory':subcategory})

def update_sub_post(request, slug):
    try:
        post = SubBlogPost.objects.get(slug=slug)
        category = BlogPostSubCategories.objects.get(id=post.subcategory_id)
        queryset = SubBlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)
        
        if request.method == "POST":
            form = SubBlogPostForm(data=request.POST, instance=post, files=request.FILES)
            if form.is_valid():
                post = form.save()
                return redirect('/en/'+ post.slug + '/sub/')
                # Future further research work
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{post.title} updated." })})
        else:
            form = SubBlogPostForm(instance=post)
    except:
        pass
    return render(request, "blog/partial_edit_sub_post.html", { 'form': form, 'post':post, 'category': category })

@login_required(login_url='/account/login')
def add_sub_comment(request, slug):
    try:
        post = SubBlogPost.objects.get(slug=slug)
        category = BlogPostSubCategories.objects.get(id=post.subcategory_id)
        if request.method == "POST":
            form = SubBlogPostForm(request.POST, files=request.FILES)
            if form.is_valid():
                subpost = form.save(commit=False)
                subpost.author = request.user
                subpost.subcategory = category
                subpost.parent = post
                subpost.save()
                return redirect('/en/'+ post.slug + '/sub/#' + str(subpost.id))
                
                ################ Future Research work
                # When the submit button is pressed, the popup should disappear and refresh the main 
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
        else:
            post.content = ''
            post.image1.name = ''
            post.image2.name = ''
            post.image3.name = ''
            post.image4.name = ''
            form = SubBlogPostForm(instance=post)
    except:
        pass
    return render(request, 'blog/partial_add_sub_comment.html', {'form': form, 'post': post, 'category': category})

def update_sub_comment(request, id):
    try:
        post = SubBlogPost.objects.get(id=id)
        if post.parent_id is not None:
            parentpost = SubBlogPost.objects.get(id=post.parent_id)
        
        category = BlogPostSubCategories.objects.get(id=post.subcategory_id)
        queryset = SubBlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        #datas = get_object_or_404(queryset, slug=slug)
        
        if request.method == "POST":
            form = SubBlogPostForm(data=request.POST, instance=post, files=request.FILES)
            if form.is_valid():
                post = form.save()
                if post.parent_id is not None:
                    return redirect('/en/'+ parentpost.slug + '/sub/')
                else:
                    return redirect('/en/'+ post.slug + '/sub/')
                # Future further research work
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{post.title} updated." })})
        else:
            form = SubBlogPostForm(instance=post)
    except:
        pass
    return render(request, "blog/partial_edit_sub_comment.html", { 'form': form, 'post':post, 'category': category })

@login_required(login_url='/account/login')
def reply_sub_post(request, id):
    post = SubBlogPost.objects.get(id=id)
    if post.parent_id is not None:
        parentpost = SubBlogPost.objects.get(id=post.parent_id)
    
    category = BlogPostSubCategories.objects.get(id=post.subcategory_id)
    
    if request.method == "POST":
        form = SubBlogPostForm(request.POST, files=request.FILES)
        if form.is_valid():
            subpost = form.save(commit=False)
            subpost.title = post.title
            subpost.subcategory = category
            subpost.author = request.user
            if post.parent_id is not None:
                subpost.parent = parentpost
            else:
                subpost.parent = post
            subpost.save()
            
            object_list = SubBlogPost.objects.filter(parent_id=post.id)
            no_of_pages = Paginating.objects.get()
            paginator = Paginator(object_list, no_of_pages.number_of_pages)
            
            if post.parent_id is not None:
                return redirect('/'+ parentpost.slug + '/sub/?page=' + str(paginator.num_pages) +'#'+str(subpost.pk))
            else:
                return redirect('/'+ post.slug + '/sub/#'+ str(subpost.pk))
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        if post.parent_id is not None:
            p = '<blockquote>' + '<p><a href=/' + parentpost.slug + '/sub/#' + str(id) + '><b>' + post.author.username + ':</b></a></p>' + post.content + '</blockquote><p></p>'
        else:
            p = '<blockquote>' + '<p><a href=/' + post.slug + '/sub/#' + str(id) + '><b>' + post.author.username + ':</b></a></p>' + post.content + '</blockquote><p></p>'

        post.content = p
        post.image1.name = ''
        post.image2.name = ''
        post.image3.name = ''
        post.image4.name = ''
        form = SubBlogPostForm(instance=post)
        
    return render(request, 'blog/partial_reply_sub_post.html', {'form': form, 'post': post, 'category': category})

def Delete_Sub_Post(request, slug):
    post = SubBlogPost.objects.get(slug=slug)
    p = BlogPostSubCategories.objects.get(id=post.subcategory_id)
    if request.method == "POST":
        if request.user == post.author:
            if check_if_less_than_seven_days(post.dateTime):
                post.delete()
            return redirect('/en/sub/'+ p.slug + '/') #TODO: This must be able to 
    return render(request, 'blog/delete_blog_post.html', {'posts': post})

#endregion

#region =============== Like post, viewed post, Search post, Shared post, mail_moderator, site_stat systems =============
# Django 3 By Example --> Page 172
@ajax_required
@login_required(login_url='/account/login')
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    slug = request.POST.get('slug')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = BlogPost.objects.get(id=post_id)
            #post = BlogPost.objects.get(slug=slug)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

@ajax_required
@login_required(login_url='/account/login')
@require_POST
def sub_post_like(request):
    post_id = request.POST.get('id')
    slug = request.POST.get('slug')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = SubBlogPost.objects.get(id=post_id)
            #post = BlogPost.objects.get(slug=slug)
            if action == 'like':
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

def post_viewed(request, slug):
    if slug:
        try:
            post = BlogPost.objects.get(slug=slug)
         
            if request.user.is_authenticated:
                post.viewers.add(request.user)
            elif request.user.is_anonymous:
                request.session['cached_session_key'] = request.session.session_key
                #post.viewers.add()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

def sub_post_viewed(request, slug):
    if slug:
        try:
            post = SubBlogPost.objects.get(slug=slug)
         
            if request.user.is_authenticated:
                post.viewers.add(request.user)
            elif request.user.is_anonymous:
                request.session['cached_session_key'] = request.session.session_key
                #post.viewers.add()
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        object_list = BlogPost.objects.filter(title__icontains=searched)
        
        # Paginate blog details
        paginator = Paginator(object_list, 30)  # 3 posts in each page
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
        
        return render(request, "blog/search.html", {'searched': searched, 'posts': posts})
    else:
        return render(request, "blog/search.html", {})

@login_required(login_url='/account/login')
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(BlogPost, id=post_id)
    sent = False
    # global form
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            #subject = f"{cd['name']} recommends you read " f"{post.title}"
            subject = f"{request.user.first_name, request.user.last_name} recommends you read " f"{post.title}"
            #message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            message = f"Read {post.title} at {post_url}\n\n" f"{request.user.first_name, request.user.last_name}\'s comments: {cd['comments']}"
            sendermail = request.user.email
            receipientmail = [cd['recepient_email']]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True
            return redirect('/en/'+ post.slug + '/')
            #return redirect('/en/{{post.slug}}/{{post.id}}')
    else:
        form = EmailPostForm()
    return render(request, 'blog/partial_share.html', {'post': post, 'form': form, 'sent': sent})

@login_required(login_url='/account/login')
def sub_post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(SubBlogPost, id=post_id)
    sent = False
    # global form
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            #subject = f"{cd['name']} recommends you read " f"{post.title}"
            subject = f"{request.user.first_name, request.user.last_name} recommends you read " f"{post.title}"
            #message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            message = f"Read {post.title} at {post_url}\n\n" f"{request.user.first_name, request.user.last_name}\'s comments: {cd['comments']}"
            sendermail = request.user.email
            receipientmail = [cd['recepient_email']]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True
            return redirect('/en/'+ post.slug + '/sub/')
            #return redirect('/en/{{post.slug}}/{{post.id}}')
    else:
        form = EmailPostForm()
    return render(request, 'blog/partial_share_sub.html', {'post': post, 'form': form, 'sent': sent})

@login_required(login_url='/account/login')
def mail_moderator(request, cat_id):
    # Retrieve post by id
    category = get_object_or_404(BlogPostCategories, id=cat_id)
    sent = False
    # global form
    if request.method == 'POST':
        # Form was submitted
        form = EmailModeratorForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            subject = f"{cd['subject']}"
            message = f"{cd['message']}"
            sendermail = request.user.email
            receipientmail = [category.moderatoremail]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True
            
            object_list = BlogPost.objects.filter(category=cat_id).order_by('-dateTime')
            paginator = Paginator(object_list, 36)  # 3 posts in each page
            page = request.GET.get('page')
            try:
                posts = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                posts = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                posts = paginator.page(paginator.num_pages)
            return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})
    else:
        form = EmailModeratorForm()
    return render(request, 'blog/partial_mail_moderator.html', {'category': category, 'form': form, 'sent': sent})


@login_required(login_url='/account/login')
def report_post(request, post_id):
    # Retrieve post by id
    post = BlogPost.objects.get(id=post_id)
    if post.parent_id is not None:
        parentpost = BlogPost.objects.get(id=post.parent_id)
        
    category = get_object_or_404(BlogPostCategories, id=post.category_id)
    sent = False
    # global form
    if request.method == 'POST':
        # Form was submitted
        form = ReportPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = "Content Breach Report. " + f"{request.user.first_name, request.user.last_name} reports breach of content."
            message = f"{cd['message']}\n\n" f"{post_url}\n\n" + post.content
            sendermail = request.user.email
            receipientmail = [category.moderatoremail]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True    
            messages.success(request, "Your report has been delivered to the moderator. Thanks for using AcrossGlobe")
            
            if post.parent_id is not None:
                return redirect('/en/'+ parentpost.slug + '/')
            else:
                return redirect('/en/'+ post.slug + '/')
            
            
            #JsonResponse({'status':'ok'})
            # object_list = BlogPost.objects.filter(category=cat_id).order_by('-dateTime')
            # paginator = Paginator(object_list, 36)  # 3 posts in each page
            # page = request.GET.get('page')
            # try:
            #     posts = paginator.page(page)
            # except PageNotAnInteger:
            #     # If page is not an integer deliver the first page
            #     posts = paginator.page(1)
            # except EmptyPage:
            #     # If page is out of range deliver last page of results
            #     posts = paginator.page(paginator.num_pages)
            # return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})
    else:
        form = ReportPostForm()
    return render(request, 'blog/partial_report_post.html', {'post': post,'category': category, 'form': form, 'sent': sent})



def site_statistics(request):
    return render(request, 'blog/partial_site_statistics.html')

#endregion

#region =============== Advertise on blog post category =================================================================
@login_required(login_url='/account/login')
def adverts(request, slug):
    category = get_object_or_404(BlogPostCategories, slug=slug)
    myadverts = get_object_or_404(Advertisement, user_id=request.user.id)
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/en/' + slug + '/' + category.id + '/')
    else:
       form = AdvertisementForm()
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'category': category, 'myadverts': myadverts})


@login_required(login_url='/account/login')
def adverts(request):
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            #form.category = post
            form.user = request.user
            form.save()
            
            #return redirect('en/' + slug + '/' + category.id + '/')
            
            # object_list = BlogPost.objects.filter(category=category.id).order_by('-dateTime')
            # paginator = Paginator(object_list, 36)  # 3 posts in each page
            # page = request.GET.get('page')
            # try:
            #     posts = paginator.page(page)
            # except PageNotAnInteger:
            #     # If page is not an integer deliver the first page
            #     posts = paginator.page(1)
            # except EmptyPage:
            #     # If page is out of range deliver last page of results
            #     posts = paginator.page(paginator.num_pages)
            #return render(request, "blog/blog_category.html", {'posts': posts, 'category': category})
            
            #return redirect('/en/partial_advertisement/{{ category_id }}'), 'myadverts': myadverts
    else:
       form = AdvertisementForm()
    return render(request, 'blog/partial_advertisement.html', {'form': form})


def edit_advertisement(request, pk):
    category = get_object_or_404(BlogPostCategories, id=request.category.id)
    advert = get_object_or_404(Advertisement, pk=pk)
    if request.method == "POST":
        form = AdvertisementForm(request.POST, instance=advert)
        if form.is_valid():
            form.save()
            return redirect('/en/partial_advertisement/{{ category_id }}')
    else:
       form = AdvertisementForm(instance=advert)
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'category': category})

#endregion

#region =============== Generate Unique code for adverts =================================================================




#endregion