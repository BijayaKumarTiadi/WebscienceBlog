import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from .forms import CommentForm
from .models import Category,BlogPost, Comment,Tag
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.cache import cache_page
from django.db.models import Count
# Create your views here.
def index(request):
    posts = BlogPost.objects.filter(is_published=True)[:11]
    cache.set('posts',posts, timeout=900)
    if posts:
        mainpost = posts[0] if posts else None
        trendingposts = [post for post in posts if post.tags.filter(name__icontains='trending').exists() and post.is_published]#remove is published
        trendingposts = sorted(trendingposts, key=lambda post: post.pub_date, reverse=True)[:1] #use it later by only selecting more than one trending post
    #if there is no trending tag between top 10 posts then there will be error .
    
    latest_posts_by_category = list(BlogPost.objects.filter(category__isnull=False,is_published=True).order_by('category', '-pub_date')[:7])
    random.shuffle(latest_posts_by_category)
    
    # categories_with_views = Category.objects.annotate(total_views=Sum('blogpost__views'))
    top_categories = cache.get('top_categories')
    cats = cache.get('cats')
    most_viewed_posts = cache.get('most_viewed_posts')
    if top_categories is None:
        cats=Category.objects.all()
        top_categories = cats.annotate(total_views=Sum('blogpost__views')).order_by('-total_views')[:6]
        most_viewed_posts = sorted(posts, key=lambda post: post.views, reverse=True)
        cache.set('top_categories', top_categories, timeout=900)
        cache.set('cats', cats, timeout=900)
        cache.set('most_viewed_posts',most_viewed_posts, timeout=900)
    data={
        'posts':posts,
        'cats':cats,
        'mainpost':mainpost,
        'latest_posts_by_category':latest_posts_by_category,
        'top_categories':top_categories,
        'most_viewed_posts':most_viewed_posts,
    }
    return render(request,"index.html",context=data)
# @cache_page(60 * 15)
def post_detail(request, category_slug, post_slug, parent_comment_id=None):
    category_obj = get_object_or_404(Category, url=category_slug)
    post = get_object_or_404(BlogPost, category=category_obj, url=post_slug)
    # post = get_object_or_404(BlogPost, category=category_obj, url=slug)#Here is url= because in the model its url
    post.views += 1
    post.save()

    trending_tags = Tag.get_trending_tags(n=9)

    top_categories = cache.get('top_categories')
    cats = cache.get('cats')
    most_viewed_posts = cache.get('most_viewed_posts')
    posts = cache.get('posts')

    if top_categories is None:
        cats=Category.objects.all()
        cache.set('cats', cats, timeout=900)

        top_categories = cats.annotate(total_views=Sum('blogpost__views')).order_by('-total_views')[:6]
        cache.set('top_categories', top_categories, timeout=900)

    if posts is None:
        posts = BlogPost.objects.filter(is_published=True)[:11]
        most_viewed_posts = sorted(posts, key=lambda post: post.views, reverse=True)
        cache.set('posts',posts, timeout=900)
        cache.set('most_viewed_posts',most_viewed_posts,timeout=900)

    you_might_also_like = random.sample(list(posts), 2)

    hierarchy = [
        {'url': '/', 'name': 'Home'},
        {'url': '/{}/'.format(category_obj.url), 'name': category_obj.url},
        {'url': '', 'name': post.url},
    ]
    #comment
    comments = post.comments.filter(approved_comment=True)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
            # Optionally, you might want to redirect or refresh the page after submitting a comment
    else:
        comment_form = CommentForm()

    context={
        'post': post,
        'hierarchy': hierarchy,
        'top_categories':top_categories,
        'most_viewed_posts':most_viewed_posts,
        'you_might_also_like':you_might_also_like,
        'trending_tags':trending_tags,
        }
    return render(request, 'postdetail.html',context )

def category_detail(request, slug):
    category = get_object_or_404(Category, url=slug)
    posts = BlogPost.objects.filter(category=category)
    return render(request, 'category_detail.html', {'category': category, 'posts': posts})


def trending_posts(request, tag_name):
    # Replace 'your_tag' with the actual trending tag name
    posts = BlogPost.objects.filter(tags__name__icontains=tag_name).order_by('-created_at')[:2]

    context = {
        'tag_name': tag_name,
        'posts': posts
    }

    return render(request, 'trending_posts.html', context)

def popular_news_view(request):
    
    most_viewed_posts = BlogPost.objects.filter(is_published=True).order_by('-views')[:50]
    paginator = Paginator(most_viewed_posts, 5)  # Adjust the number of posts per page as needed
    page = request.GET.get('page')
    try:
        most_viewed_posts = paginator.page(page)
    except PageNotAnInteger:
        most_viewed_posts = paginator.page(1)
    except EmptyPage:
        most_viewed_posts = paginator.page(paginator.num_pages)

    context = {'most_viewed_posts': most_viewed_posts,
                }
    return render(request, 'popular_news.html', context)

def author_posts(request, author_name):
    #Fetch all posts by auther name from the posts
    author = get_object_or_404(User, username=author_name)
    author_posts = BlogPost.objects.filter(author=author,is_published=True).order_by('-pub_date')
    context={
        'author_posts':author_posts,
        'author_name':author_name
    }
    return render(request, 'author_posts.html', context)

def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = BlogPost.objects.filter(tags=tag)
    return render(request, 'tagposts.html', {'tag': tag, 'posts': posts})

def custom_404(request, exception):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response
# @login_required
def contact_us(request):
    aboutme={}
    return render(request,"contact-us.html",context=aboutme)