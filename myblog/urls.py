from django.conf import settings
from django.urls import path, re_path as url
from . import views
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django.contrib import admin


app_name = 'MyBlog'

urlpatterns = [
    
    #   Administrative Areas
    path(_('admin/'), admin.site.urls),
    
    #   Advertisement
    path(_('adverts/'), views.adverts, name="adverts"),                                                #   blog/partial_advertisement.html
    
    #   Category list by type
    path(_('cat/<int:pk>/'), views.category_by_type, name="category_by_type"), 
    
    #   Category
    path(_('add_category/'), views.add_category, name="category"),                                     #   blog/add_categories.html                    *           
    path(_('category_list/'), views.category_list, name="category_list"),                              #   blog/add_categories.html                    *
    path(_('edit_category/<int:pk>'), views.edit_category, name="edit_category"),                      #   blog/partial_edit_category.html             *
    
    #   Blogs list
    path("", views.blogs_list, name="blogs"),
    path(_("news/"), views.news_list, name="news"),
    
    #   Blogs by Category
    path(_('<str:slug>/<int:cat_id>/'), views.blogByCategory, name="blogs_Category"),                   #   blog/blog_list.html                         *DONE
    path(_('<str:slug>/'), views.blog_details, name="blog_details"),                                    #   blog/blog_details.html                      *DONE
    path(_('<int:cat_id>/newtopic/'), views.add_post, name="add_post"),                                 #   blog/partial_add_newtopic.html              *DONE
    path(_('edit_blog_post/<str:slug>/'), views.update_post, name="update_post"),                       #   blog/partial_edit_blog_post.html            *DONE
    path(_('delete_post/<str:slug>/'), views.Delete_Post, name="delete_post"),                          #   blog/delete_blog_post.html                  *DONE

    #   Post Comment Reply System
    path(_('add_comment/<str:slug>/'), views.add_comment, name="add_comment"),                          #   blog/partial_add_comment.html               *
    path(_('<int:id>/update_comment/'), views.update_comment, name="update_comment"),                   #   blog/partial_add_comment.html     
    path(_('<int:id>/reply_post/'), views.reply_post, name="reply_post"),                               #   blog/partial_reply_post.html 
    
    #   Sub Posts
    path(_('sub/<str:slug>/'), views.blogBySubCategory, name="blogs_sub_category"),                      #   blog/blog_sub_category.html                 *DONE
    path(_('<str:slug>/sub/'), views.blog_sub_details, name="blog_sub_details"),                         #   blog/blog_sub_details.html                  *DONE
    path(_('<int:subcat_id>/subtopic/'), views.add_sub_post, name="add_sub_post"),                       #   blog/partial_add_subtopic.html              *DONE
    path(_('sub/edit_sub_post/<str:slug>/'), views.update_sub_post, name="update_sub_post"),             #   blog/partial_edit_sub_blog_post.html        *DONE
    path(_('sub/delete_sub_post/<str:slug>/'), views.Delete_Sub_Post, name="delete_sub_post"),           #   blog/delete_blog_post.html                  *DONE, but needs further adjustment

    #   Sub post Comment Reply System
    path(_('sub/add_sub_comment/<str:slug>/'), views.add_sub_comment, name="add_sub_comment"),           #   
    path(_('sub/update_sub_comment/<int:id>/'), views.update_sub_comment, name="update_sub_comment"),    #                               
    path(_('sub/reply_sub_post/<int:id>/'), views.reply_sub_post, name="reply_sub_post"),                #   blog/partial_reply_sub_post.html            *DONE
   
    
    #   email moderator
    path(_('<int:cat_id>/mailmoderator/'), views.mail_moderator, name='mail_moderator'),                 #   blog/partial_mail_moderator.html
    path(_('<int:post_id>/report_post/'), views.report_post, name="report_post"),
    
    #   Like and Unlike
    path(_('blog/like/'), views.post_like, name='like'),                                                      #   
    
     #   Like and Unlike
    path(_('blog/like/sub'), views.sub_post_like, name='sublike'),
    
    #   Search
    path(_('con/search/'), views.search, name="search"),                                                 #   blog/search.html
   
    #   Share post via email
    path('<int:post_id>/share/', views.post_share, name='post_share'),                                   #   blog/partial_share.html
    
    #   Share post via email
    path('<int:post_id>/share/sub/', views.sub_post_share, name='sub_post_share'), 
    
    #   Site Statistics
    path('stat/', views.site_statistics, name='site_statistics'),                                        #   blog/partial_site_statistics.html
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
