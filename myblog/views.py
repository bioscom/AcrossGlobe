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
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from datetime import timedelta
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile


class AllKeywordsView(ListView):
    model = BlogPost
    template_name = "blog/blog.html"


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

#region =============== Category ========================================================================================
def category_list(request):
    try:
        categories = BlogPostCategories.objects.all().order_by('type')
        subcategories = BlogPostSubCategories.objects.all()
        form = CategoryForm(data=request.POST, files=request.FILES)
        #return render(request, "blog/add_categories.html", {'form': form, 'categories': categories})
    except:
        pass
    return render(request, "blog/add_categories.html", {'form': form, 'categories': categories, 'subcategories': subcategories})

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


#region =============== Add New Post(new topic), Update and Delete post =================================================

@login_required(login_url='/account/login')
def add_newtopic(request, cat_id):
    try:
        category = BlogPostCategories.objects.get(id=cat_id)  
        # BlogPostCategories.objects.get(id=cat_id)
        # BlogPostCategories.objects.filter(slug=slug).first()
        object_list = BlogPost.objects.all()
        posts = BlogPost.objects.filter(category=cat_id).order_by('-dateTime')
        data = dict()
        
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, files=request.FILES)
            
            formset1 = FileUploadForm(data=request.POST, files=request.FILES)
            formset2 = FileUploadForm(data=request.POST, files=request.FILES)
            formset3 = FileUploadForm(data=request.POST, files=request.FILES)
            formset4 = FileUploadForm(data=request.POST, files=request.FILES)
            
            if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
                blogpost = form.save(commit=False)
                blogpost.author = request.user
                blogpost.category = category
                blogpost.save()
                files = Upload_Files(request, blogpost.id)
                add_image_newtopic(blogpost, files)
                
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
                
                ################ Future Research work
                # When the submit button is pressed, the popup should disappear and refresh the main 
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
        else:
            form = BlogPostForm()
            formset1 = FileUploadForm()
            formset2 = FileUploadForm()
            formset3 = FileUploadForm()
            formset4 = FileUploadForm()
    except:
        pass
    return render(request, "blog/partial_add_newtopic.html", {'form': form, 'formset1': formset1, 'formset2': formset2, 'formset3': formset3, 'formset4': formset4, 'category': category})

def update_post(request, slug):
    try:
        post = BlogPost.objects.get(slug=slug)
        category = BlogPostCategories.objects.get(id=post.category_id)
        
        queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)
        comments = Comment.objects.filter(blog=post)
        
        if request.method == "POST":
            form = BlogPostForm(data=request.POST, instance=post, files=request.FILES)
            
            formset1 = FileUploadForm(data=request.POST, files=request.FILES)
            formset2 = FileUploadForm(data=request.POST, files=request.FILES)
            formset3 = FileUploadForm(data=request.POST, files=request.FILES)
            formset4 = FileUploadForm(data=request.POST, files=request.FILES)
            
            if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
                post = form.save()
                uploadfiles = Upload_Files(request, post.id)
                add_image_newtopic(post, uploadfiles)
                
                commentfiles = CommentFileUploads.objects.none()
                for comment in comments:
                    commentfiles = commentfiles | CommentFileUploads.objects.filter(comment_id=comment.id)  # Queryset union using | operator in Django
                
                return redirect('/en/'+ post.slug + '/')
                # Future further research work
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{post.title} updated." })})
        else:
            files = FileUploads.objects.filter(post_id=post.id)
            form = BlogPostForm(instance=post)
           
            if files.count() == 1: formset1 = FileUploadForm(instance=files[0])
            else: formset1 = FileUploadForm()
                
            if files.count() == 2: formset2 = FileUploadForm(instance=files[1])
            else: formset2 = FileUploadForm()
                
            if files.count() == 3: formset3 = FileUploadForm(instance=files[2])
            else: formset3 = FileUploadForm()
                
            if files.count() == 4: formset4 = FileUploadForm(instance=files[3])
            else: formset4 = FileUploadForm()
    except:
        pass
    return render(request, "blog/partial_edit_blog_post.html", {
        'form': form, 'formset1': formset1, 'formset2': formset2,
        'formset3': formset3,'formset4': formset4,'post':post, 'category': category
        })

@login_required(login_url='en/account/login')
def reply_post(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    category = BlogPostCategories.objects.filter(id=post.category_id).first()
    files = FileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, files=request.FILES)
        formset1 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            comment = form.save(commit=False)
            comment.blog = post
            comment.user = request.user
            comment.save()
            Comment_Upload_Files(request, comment.id)
            
            return redirect('/en/'+ post.slug + '/')
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        #files = CommentFileUploads.objects.filter(comment_id=comment.id)
        #form = Reply_CommentForm2(instance=comment)
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + post.content + '</blockquote>'
        post.content = p
        form = Reply_CommentForm(instance=post)
        formset1 = CommentFileUploadForm()
        formset2 = CommentFileUploadForm()
        formset3 = CommentFileUploadForm()
        formset4 = CommentFileUploadForm()
        
    return render(request, 'blog/partial_reply_post.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'category': category})
 
def add_image_newtopic(blogpost, file):
    try:
        if (len(file) > 0):
            # check to see which file is image ie., jpeg or png
            for f in file:
               if f.content_type == 'image/png' or f.content_type == 'image/jpeg' or f.content_type == 'image/bmp' or f.content_type == 'image/x-png' or f.content_type == 'image/gif':
                    blogpost.image = f 
                    img = Image.open(f)
                    img.thumbnail((90,90))
                    blogpost.thumbnails = img
                    break
            blogpost.save()
            return HttpResponse('')
        else:
            return HttpResponse('')
    except:
        pass

def Delete_Post(request, slug):
    post = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        if request.user == post.user:
            if check_if_less_than_seven_days(post.dateTime):
                post.delete()
            return redirect('/')
    return render(request, 'blog/delete_blog_post.html', {'posts': post})

def Upload_Files(request, post_id):
    try:
        form = FileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = FileUploads(file=f)
                    file_instance.post_id = post_id
                    file_instance.save()
        else:
            form = FileUploadForm()
    except:
        pass
    return files

#endregion

#region =============== Add Comment to blog post ========================================================================

@login_required(login_url='/account/login')
def add_comment(request, slug):
    #try:
    post = BlogPost.objects.filter(slug=slug).first()

    category = BlogPostCategories.objects.filter(id=post.category_id).first()
    comments = Comment.objects.filter(blog=post)
    files = FileUploads.objects.filter(post_id=post.id)
    queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    datas = get_object_or_404(queryset, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        formset1 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            comment = form.save(commit=False)
            comment.user = request.user
            comment.blog = post
            comment.save()
            Comment_Upload_Files(request, comment.id)

            # commentfiles = CommentFileUploads.objects.none()
            # for comment in comments:
            #     commentfiles = commentfiles | CommentFileUploads.objects.filter(comment_id=comment.id)
            # commentfiles = CommentFileUploads.objects.filter(comment_id=comment.id)
            
            return redirect('/en/'+ post.slug + '/')
            
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        # p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + post.content + '</blockquote>'
        # post.content = p
        form = CommentForm()
        formset1 = CommentFileUploadForm()
        formset2 = CommentFileUploadForm()
        formset3 = CommentFileUploadForm()
        formset4 = CommentFileUploadForm()
    #except:
    #    pass
    return render(request, 'blog/partial_add_comment.html', {
        'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 
        'post': post, 'category': category})

def Comment_Upload_Files(request, comment_id):
    try:
        form = CommentFileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = CommentFileUploads(file=f)
                    file_instance.comment_id = comment_id
                    file_instance.save()
        else:
            form = CommentFileUploadForm()
    except:
        pass
    return files

@login_required(login_url='en/account/login')
def reply_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = BlogPost.objects.filter(id=comment.blog_id).first()
    category = BlogPostCategories.objects.filter(id=post.category_id).first()
    files = FileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = Reply_CommentForm(request.POST, files=request.FILES)
        formset1 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = CommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            reply_comment = form.save(commit=False)
            reply_comment.blog = post
            reply_comment.user = request.user
            reply_comment.parent = comment
            reply_comment.save()
            Comment_Upload_Files(request, comment.id)
            
            #replycomment = Comment.objects.filter(parent=comment_id)
            #messages.success(request, 'Comment replied!')
            
            return redirect('/en/'+ post.slug + '/')
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        #files = CommentFileUploads.objects.filter(comment_id=comment.id)
        #form = Reply_CommentForm2(instance=comment)
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + comment.content + '</blockquote>'
        comment.content = p
        form = Reply_CommentForm(instance=comment)
        formset1 = CommentFileUploadForm()
        formset2 = CommentFileUploadForm()
        formset3 = CommentFileUploadForm()
        formset4 = CommentFileUploadForm()
        
    return render(request, 'blog/partial_add_reply_comment.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'comments': comment, 'category': category})

@login_required(login_url='en/account/login')
def update_reply_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    post = BlogPost.objects.filter(id=comment.blog_id).first()
    category = BlogPostCategories.objects.filter(id=post.category_id).first()
    files = FileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = Reply_CommentForm(data=request.POST, files=request.FILES)
        
        
        if form.is_valid():
            formset1 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            formset2 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            formset3 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            formset4 = CommentFileUploadForm(data=request.POST, files=request.FILES)
            
            form.save()
            Comment_Upload_Files(request, comment.id)
            return redirect('/en/'+ post.slug + '/')
        
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        files = CommentFileUploads.objects.filter(comment_id=comment.id)
        
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + comment.content + '</blockquote>'
        comment.content = p
        form = Reply_CommentForm(instance=comment)
        
        if files.count() == 1: formset1 = CommentFileUploadForm(instance=files[0]) 
        else: formset1 = CommentFileUploadForm()
            
        if files.count() == 2: formset2 = CommentFileUploadForm(instance=files[1])
        else: formset2 = CommentFileUploadForm()
            
        if files.count() == 3: formset3 = CommentFileUploadForm(instance=files[2])
        else: formset3 = CommentFileUploadForm()
            
        if files.count() == 4: formset4 = CommentFileUploadForm(instance=files[3])
        else: formset4 = CommentFileUploadForm()
            
    return render(request, 'blog/partial_edit_reply_comment.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'comments': comment, 'category': category})

#endregion


#region =============== Add New SubPost(sub topic), Update and Delete sub post =================================================

@login_required(login_url='/account/login')
def add_subtopic(request, id):
    try:
        subcategory = BlogPostSubCategories.objects.get(id=id) 
        category = BlogPostCategories.objects.get(id=subcategory.category_id)  
        object_list = SubBlogPost.objects.all()
        posts = SubBlogPost.objects.filter(subcategory=subcategory.id).order_by('-dateTime')
        
        if request.method == "POST":
            form = SubBlogPostForm(data=request.POST, files=request.FILES)
            
            formset1 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset2 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset3 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset4 = SubFileUploadForm(data=request.POST, files=request.FILES)
            
            if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
                blogpost = form.save(commit=False)
                blogpost.author = request.user
                blogpost.subcategory = subcategory
                blogpost.save()
                files = Sub_Upload_Files(request, blogpost.id)
                add_image_newtopic(blogpost, files)
                
                return redirect('/en/sub/'+ subcategory.slug +'/')
                
                ################ Future Research work
                # When the submit button is pressed, the popup should disappear and refresh the main 
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
        else:
            form = SubBlogPostForm()
            formset1 = SubFileUploadForm()
            formset2 = SubFileUploadForm()
            formset3 = SubFileUploadForm()
            formset4 = SubFileUploadForm()
    except:
        pass
    return render(request, "blog/partial_add_subtopic.html", {'form': form, 'formset1': formset1, 'formset2': formset2, 'formset3': formset3, 'formset4': formset4, 'category': category, 'subcategory':subcategory})

def update_sub_post(request, slug):
    try:
        post = SubBlogPost.objects.get(slug=slug)
        category = BlogPostSubCategories.objects.get(id=post.subcategory_id)
        
        queryset = SubBlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
        datas = get_object_or_404(queryset, slug=slug)
        comments = SubComment.objects.filter(blog=post)
        
        if request.method == "POST":
            form = SubBlogPostForm(data=request.POST, instance=post, files=request.FILES)
            
            formset1 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset2 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset3 = SubFileUploadForm(data=request.POST, files=request.FILES)
            formset4 = SubFileUploadForm(data=request.POST, files=request.FILES)
            
            if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
                post = form.save()
                uploadfiles = Sub_Upload_Files(request, post.id)
                add_image_newtopic(post, uploadfiles)
                
                commentfiles = SubCommentFileUploads.objects.none()
                for comment in comments:
                    commentfiles = commentfiles | SubCommentFileUploads.objects.filter(comment_id=comment.id)  # Queryset union using | operator in Django
                
                return redirect('/en/'+ post.slug + '/sub/')
                # Future further research work
                # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{post.title} updated." })})
        else:
            files = SubFileUploads.objects.filter(post_id=post.id)
            form = SubBlogPostForm(instance=post)
           
            if files.count() == 1: formset1 = SubFileUploadForm(instance=files[0])
            else: formset1 = SubFileUploadForm()
                
            if files.count() == 2: formset2 = SubFileUploadForm(instance=files[1])
            else: formset2 = SubFileUploadForm()
                
            if files.count() == 3: formset3 = SubFileUploadForm(instance=files[2])
            else: formset3 = SubFileUploadForm()
                
            if files.count() == 4: formset4 = SubFileUploadForm(instance=files[3])
            else: formset4 = SubFileUploadForm()
    except:
        pass
    return render(request, "blog/partial_edit_sub_blog_post.html", { 
        'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3,'formset4': formset4,'post':post, 'category': category 
        })

@login_required(login_url='en/account/login')
def reply_sub_post(request, slug):
    post = SubBlogPost.objects.filter(slug=slug).first()
    category = BlogPostSubCategories.objects.filter(id=post.subcategory_id).first()
    files = SubFileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = SubCommentForm(request.POST, files=request.FILES)
        formset1 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
            
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            comment = form.save(commit=False)
            comment.blog = post
            comment.user = request.user
            comment.save()
            SubComment_Upload_Files(request, comment.id)
            
            return redirect('/en/'+ post.slug + '/sub/')
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        #files = CommentFileUploads.objects.filter(comment_id=comment.id)
        #form = Reply_CommentForm2(instance=comment)
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + post.content + '</blockquote>'
        post.content = p
        form = SubCommentForm(instance=post)
        formset1 = SubCommentFileUploadForm()
        formset2 = SubCommentFileUploadForm()
        formset3 = SubCommentFileUploadForm()
        formset4 = SubCommentFileUploadForm()
        
    return render(request, 'blog/partial_reply_sub_post.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'category': category})

def Delete_Sub_Post(request, slug):
    post = SubBlogPost.objects.get(slug=slug)
    p = BlogPostSubCategories.objects.get(id=post.subcategory_id)
    if request.method == "POST":
        if request.user == post.author:
            if check_if_less_than_seven_days(post.dateTime):
                post.delete()
            return redirect('/en/sub/'+ p.slug + '/') #TODO: This must be able to 
    return render(request, 'blog/delete_blog_post.html', {'posts': post})

def check_if_less_than_seven_days(x):
    d = datetime.datetime.strptime(x, "%Y-%m-%d") # Add .date() if hour doesn't matter
    now = datetime.datetime.now()                 # Add .date() if hour doesn't matter
    return (d - now).days < 7

def Sub_Upload_Files(request, post_id):
    try:
        form = SubFileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = SubFileUploads(file=f)
                    file_instance.post_id = post_id
                    file_instance.save()
        else:
            form = SubFileUploadForm()
    except:
        pass
    return files

#endregion

#region =============== Add Comment to blog sub post ========================================================================

@login_required(login_url='en/account/login')
def reply_sub_comment(request, comment_id):
    comment = SubComment.objects.get(id=comment_id)
    post = SubBlogPost.objects.filter(id=comment.blog_id).first()
    category = BlogPostSubCategories.objects.filter(id=post.subcategory_id).first()
    files = SubFileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = Reply_SubCommentForm(request.POST, files=request.FILES)
        formset1 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
            
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            reply_comment = form.save(commit=False)
            reply_comment.blog = post
            reply_comment.user = request.user
            reply_comment.parent = comment
            reply_comment.save()
            SubComment_Upload_Files(request, comment.id)
            
            return redirect('/en/'+ post.slug + '/sub/')
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        #files = CommentFileUploads.objects.filter(comment_id=comment.id)
        #form = Reply_CommentForm2(instance=comment)
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + comment.content + '</blockquote>'
        comment.content = p
        form = Reply_SubCommentForm(instance=comment)
        formset1 = SubCommentFileUploadForm()
        formset2 = SubCommentFileUploadForm()
        formset3 = SubCommentFileUploadForm()
        formset4 = SubCommentFileUploadForm()
        
    return render(request, 'blog/partial_reply_sub_comment.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'comments': comment, 'category': category})

@login_required(login_url='en/account/login')
def update_reply_sub_comment(request, comment_id):
    comment = SubComment.objects.get(id=comment_id)
    post = SubBlogPost.objects.filter(id=comment.blog_id).first()
    category = BlogPostSubCategories.objects.filter(id=post.subcategory_id).first()
    files = SubFileUploads.objects.filter(post_id=post.id)
    
    if request.method == "POST":
        form = Reply_SubCommentForm(data=request.POST, files=request.FILES)
        formset1 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset2 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset3 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        formset4 = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        
        if all([form.is_valid(), formset1.is_valid(), formset2.is_valid(), formset3.is_valid(), formset4.is_valid()]):
            
            reply_comment = form.save(commit=False)
            reply_comment.blog = post
            reply_comment.user = request.user
            reply_comment.parent = comment
            form.save()
            SubComment_Upload_Files(request, comment.id)
            return redirect('/en/'+ post.slug + '/sub/')
        
            ################ Future Research work
            # When the submit button is pressed, the popup should disappear and refresh the main 
            # return HttpResponse(status=204, headers={'HX-Trigger': json.dumps({"postChanged": None, "showMessage": f"{request.title} updated." })})
    else:
        files = SubCommentFileUploads.objects.filter(comment_id=comment.id)
        
        p = '<blockquote author='+ post.author.username + ' slug=' + post.slug + '>' + comment.content + '</blockquote>'
        comment.content = p
        form = Reply_SubCommentForm(instance=comment)
        
        if files.count() == 1: formset1 = SubCommentFileUploadForm(instance=files[0]) 
        else: formset1 = SubCommentFileUploadForm()
            
        if files.count() == 2: formset2 = SubCommentFileUploadForm(instance=files[1])
        else: formset2 = SubCommentFileUploadForm()
            
        if files.count() == 3: formset3 = SubCommentFileUploadForm(instance=files[2])
        else: formset3 = SubCommentFileUploadForm()
            
        if files.count() == 4: formset4 = SubCommentFileUploadForm(instance=files[3])
        else: formset4 = SubCommentFileUploadForm()
            
    return render(request, 'blog/partial_edit_reply_subcomment.html', {'form': form, 'formset1': formset1, 'formset2': formset2, 
        'formset3': formset3, 'formset4': formset4, 'post': post, 'comments': comment, 'category': category})

def SubComment_Upload_Files(request, comment_id):
    try:
        form = SubCommentFileUploadForm(data=request.POST, files=request.FILES)
        files = request.FILES.getlist('file')
        if request.method == 'POST':
            if form.is_valid():
                for f in files:
                    file_instance = SubCommentFileUploads(file=f)
                    file_instance.comment_id = comment_id
                    file_instance.save()
        else:
            form = SubCommentFileUploadForm()
    except:
        pass
    return files

#endregion


#region =============== List blog posts, List blog posts by category and blog details ===============================

def blogs_list(request):
    # Catch an anonymous user as he hits the site.
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
        
    active_users = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=10)).count()
    #active_anonymous = User.objects.all().filter(last_login__gte=now()-timedelta(minutes=5)).count()
    
    types = TypeCategories.objects.all()
    categories = BlogPostCategories.objects.all() #.order_by('category_title')
    categories = BlogPostCategories.objects.filter() #.order_by('category_title')
    file_list = FileUploads.objects.all()
    #object_list = BlogPost.objects.all()
    object_list1 = BlogPost.objects.filter(is_approved=True).order_by('-dateTime', 'category')
    object_list2 = SubBlogPost.objects.filter(is_approved=True).order_by('-dateTime', 'subcategory')
    #object_list = object_list1 | object_list2
    paginator = Paginator(object_list1, 36)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/blog_list.html", {'posts': posts, 'types': types, 'categories': categories, 'files': file_list, 'active_users':active_users})

def blogByCategory(request, slug, cat_id):
    # Catch an anonymous user as he hits the site.
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
        
    # categories = BlogPostCategories.objects.all()
    category = BlogPostCategories.objects.filter(slug=slug).first()
    subcategories = BlogPostSubCategories.objects.all()
    object_list = BlogPost.objects.all()
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
    return render(request, "blog/blog_category.html", {'posts': posts, 'category': category, 'subcategories': subcategories })

def blogBySubCategory(request, slug):
    # Catch an anonymous user as he hits the site.
    if request.user.is_anonymous:
        request.session['cached_session_key'] = request.session.session_key
        
    # categories = BlogPostCategories.objects.all()
    subcategory = BlogPostSubCategories.objects.filter(slug=slug).first()
    category = BlogPostCategories.objects.filter(id=subcategory.category_id).first()
    
    object_list = SubBlogPost.objects.all()
    object_list = SubBlogPost.objects.filter(subcategory=subcategory.id).order_by('-dateTime')
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
    return render(request, "blog/blog_sub_category.html", {'posts': posts, 'category': category, 'subcategories': subcategory })

def blog_details(request, slug): 
    post = BlogPost.objects.filter(slug=slug).first()
    
    # To know how many authenticated users and anonymous users that viewed the post.
    post_viewed(request=request, slug=slug) 
    
    #category = BlogPostCategories.objects.none()
    #files = FileUploads.objects.none()
    if post is not None:
        category = BlogPostCategories.objects.filter(id=post.category_id).first()
        files = FileUploads.objects.filter(post_id=post.id)
        
    queryset = BlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    datas = get_object_or_404(queryset, slug=slug)
    object_list = Comment.objects.filter(blog=post).order_by('dateTime')
        # replycomment = ReplyComment.objects.none()
        # for comment in comments:
        #     replycomment = replycomment | ReplyComment.objects.filter(comment_id=comment.id)    # Queryset union using | operator in Django
    commentfiles = CommentFileUploads.objects.none()
    for comment in object_list:
        commentfiles = commentfiles | CommentFileUploads.objects.filter(comment_id=comment.id)  # Queryset union using | operator in Django
        
    # Paginate blog details
    paginator = Paginator(object_list, 36)  # 3 posts in each page
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
    return render(request, "blog/blog_details.html", {'post': post, 'comments': comments, 'datas': datas, 'commentfiles': commentfiles, 'files': files, 'category': category})

def blog_sub_details(request, slug): 
    post = SubBlogPost.objects.filter(slug=slug).first()
    
    # To know how many authenticated users and anonymous users that viewed the post.
    post_viewed(request=request, slug=slug) 
    
    #category = BlogPostCategories.objects.none()
    #files = FileUploads.objects.none()
    if post is not None:
        category = BlogPostSubCategories.objects.filter(id=post.subcategory_id).first()
        files = SubFileUploads.objects.filter(post_id=post.id)
        
    queryset = SubBlogPost.objects.annotate(num_views=Count('viewers')).order_by('-num_views')
    datas = get_object_or_404(queryset, slug=slug)
    object_list = SubComment.objects.filter(blog=post).order_by('dateTime')
        
    commentfiles = SubCommentFileUploads.objects.none()
    for comment in object_list:
        commentfiles = commentfiles | SubCommentFileUploads.objects.filter(comment_id=comment.id)  # Queryset union using | operator in Django
        
    # Paginate blog details
    paginator = Paginator(object_list, 36)  # 3 posts in each page
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
    return render(request, "blog/blog_Sub_details.html", {'post': post, 'comments': comments, 'datas': datas, 'commentfiles': commentfiles, 'files': files, 'category': category})

#endregion

#region =============== Like post, viewed post, Search post, Shared post, mail_moderator, site_stat systems =============
@ajax_required
@login_required(login_url='en/account/login')
@require_POST
def post_like(request):
    post_id = request.POST.get('id')
    slug = request.POST.get('slug')
    action = request.POST.get('action')
    if post_id and action:
        try:
            #post = BlogPost.objects.get(id=post_id)
            post = BlogPost.objects.get(slug=slug)
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

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "blog/search.html", {'searched': searched, 'blogs': blogs})
    else:
        return render(request, "blog/search.html", {})

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
            #post_url = post.get_absolute_url()
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            sendermail = request.user.email
            receipientmail = [cd['recepient_email']]
            send_mail(subject, message, sendermail, receipientmail)
            sent = True
            return redirect('/en/'+ post.slug + '/')
            #return redirect('/en/{{post.slug}}/{{post.id}}')
    else:
        form = EmailPostForm()
    return render(request, 'blog/partial_share.html', {'post': post, 'form': form, 'sent': sent})


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
            
            object_list = BlogPost.objects.filter(category=category.id).order_by('-dateTime')
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
            
            #return redirect('/en/partial_advertisement/{{ category_id }}')
    else:
       form = AdvertisementForm()
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'category': category, 'myadverts': myadverts})

@login_required(login_url='/account/login')
def advertise(request):
    #category = get_object_or_404(BlogPostCategories, slug=slug)
    myadverts = get_object_or_404(Advertisement, user_id=request.user.id)
    if request.method == "POST":
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            form.save()
            
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
            
            #return redirect('/en/partial_advertisement/{{ category_id }}')
    else:
       form = AdvertisementForm()
    return render(request, 'blog/partial_advertisement.html', {'form': form, 'myadverts': myadverts})

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

class PostDetailView(HitCountDetailView):
    model = BlogPost
    template_name = 'blog/blog_details.html'
    context_object_name = 'blogpost'
    slug_field = 'slug'
    # set to True to count the hit
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context.update({
        'popular_posts': BlogPost.objects.order_by('-hit_count_generic__hits')[:3],
        })
        return context

class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'blog/partial_edit_blog_post.html'
    fields = ['title', 'content', 'image']
    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        #'content': forms.CharField(widget=CKEditorWidget()),
        # 'content': RichTextFormField(config_name='default'), 
    }