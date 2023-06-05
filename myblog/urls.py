from django.conf import settings
from django.urls import path, re_path as url
from . import views
from .views import UpdatePostView
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _

from django.views.generic import TemplateView
from django.contrib import admin
#from posts.views import PostListView, PostDetailView

app_name = 'MyBlog'

urlpatterns = [
    
    #   Administrative Areas
    path(_('admin/'), admin.site.urls),
    
    #   Category
    path(_('add_category/'), views.add_category, name="category"),                                                              #   blog/add_categories.html                    *           
    path(_('category_list/'), views.category_list, name="category_list"),                                                       #   blog/add_categories.html                    *
    path(_('edit_category/<int:pk>'), views.edit_category, name="edit_category"),                                               #   blog/partial_edit_category.html             *
    
    #   blogs list
    path("", views.blogs_list, name="blogs"),
    path(_('<str:slug>/<int:cat_id>/'), views.blogByCategory, name="blogs_Category"),                                           #   blog/blog_list.html                         *DONE
    path(_('<str:slug>/'), views.blog_details, name="blog_details"),                                                            #   blog/blog_details.html                      *DONE
    path(_('<int:cat_id>/newtopic/'), views.add_newtopic, name="add_newtopic"),                                                 #   blog/partial_add_newtopic.html              *DONE
    path(_('edit_blog_post/<str:slug>/'), views.update_post, name="update_post"),                                               #   blog/partial_edit_blog_post.html            *DONE
    path(_('delete_post/<str:slug>/'), views.Delete_Post, name="delete_post"),                                                  #   blog/delete_blog_post.html                  *DONE
    
    #   Reply posts
    path(_('reply_post/<str:slug>/'), views.reply_post, name="reply_post"),                                                     #   blog/partial_reply_post.html                *
    #   Comment Reply System
    path(_('add_comment/<str:slug>/'), views.add_comment, name="add_comment"),                                                  #   blog/partial_add_comment.html               *
    path(_('reply_comment/<int:comment_id>'), views.reply_comment, name="reply_comment"),                                       #   blog/partial_add_reply_comment.html         *
    path(_('update_reply_comment/<int:comment_id>/'), views.update_reply_comment, name="update_reply_comment"),                 #   blog/partial_edit_reply_comment.html        *
    
    #   Sub Posts
    path(_('sub/<str:slug>/'), views.blogBySubCategory, name="blogs_sub_category"),                                             #   blog/blog_sub_category.html                 *DONE
    path(_('<str:slug>/sub/'), views.blog_sub_details, name="blog_sub_details"),                                                #   blog/blog_sub_details.html                  *DONE
    path(_('<int:id>/subtopic/'), views.add_subtopic, name="add_subtopic"),                                                     #   blog/partial_add_subtopic.html              *DONE
    path(_('sub/edit_sub_post/<str:slug>/'), views.update_sub_post, name="update_sub_post"),                                    #   blog/partial_edit_sub_blog_post.html        *DONE
    path(_('sub/reply_sub_post/<str:slug>/'), views.reply_sub_post, name="reply_sub_post"),                                     #   blog/partial_reply_sub_post.html            *DONE
    path(_('sub/reply_sub_comment/<int:comment_id>/'), views.reply_sub_comment, name="reply_sub_comment"),                      #   blog/partial_reply_sub_comment.html         *DONE
    path(_('sub/update_reply_sub_comment/<int:comment_id>/'), views.update_reply_sub_comment, name="update_reply_sub_comment"), #   blog/partial_edit_reply_subcomment.html     *DONE
    path(_('sub/delete_sub_post/<str:slug>/'), views.Delete_Sub_Post, name="delete_sub_post"),                                  #   blog/delete_blog_post.html                  *DONE, but needs further adjustment

    
    #   email moderator
    path(_('<int:cat_id>/mailmoderator/'), views.mail_moderator, name='mail_moderator'),                                        #   blog/partial_mail_moderator.html
    
    #   Like and Unlike
    path(_('like/'), views.post_like, name='like'),                                                                             #   
    
    #   Search
    path(_('search/'), views.search, name="search"),                                                                            #   blog/search.html
   
    #   Share post via email
    path('<int:post_id>/share/', views.post_share, name='post_share'),                                                          #   blog/partial_share.html
    
    #   Advertisement
    path(_('ad/'), views.advertise, name="advertise"),                                                                          #   blog/partial_advertisement.html
    path(_('<str:slug>/adverts/'), views.adverts, name="ad_adverts"),                                                           #   blog/partial_advertisement.html
    
    #   Site Statistics
    path('stat/', views.site_statistics, name='site_statistics'),                                                               #   blog/partial_site_statistics.html
    
    #path(_('reply_comment/<str:slug>/<int:comment_id>/'), views.reply_comment, name="reply_comment"),
    #path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),

    #   User's list view. Follow System part
    #path(_('users/'), views.user_list, name='user_list'),
    #path(_('users/<username>/'), views.user_detail, name='user_detail'),
    
    #path(_('infinite_scrolling'), views.AllKeywordsView.as_view(template_name="blog.html"), ), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
