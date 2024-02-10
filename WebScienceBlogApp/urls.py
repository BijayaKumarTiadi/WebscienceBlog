from django.conf import settings
from django.http import Http404
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.views.defaults import page_not_found
from .views import  author_posts, contact_us, index, popular_news_view, post_detail,category_detail, tag_posts

urlpatterns = [
    path('', index),
    path('index', index),
    path('popular-news/', popular_news_view, name='popular_news'),
    path('contact-us/', contact_us, name='contact_us'),
    path('tag/<str:tag_name>/', tag_posts, name='tag_posts'),
    path('profile/author/<str:author_name>/', author_posts, name='author_posts'),
    path('<slug:slug>/', category_detail, name='category_detail'),
    path('<slug:category_slug>/<slug:post_slug>/', post_detail, name='post_detail'),
]
