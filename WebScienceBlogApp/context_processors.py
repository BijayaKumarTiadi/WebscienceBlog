from .models import BlogPost, Category


def common_navbardata(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-pub_date')[:11]
    trendingposts = [post for post in posts if post.tags.filter(name__icontains='trending').exists() and post.is_published]#remove is published
    trendingposts = sorted(trendingposts, key=lambda post: post.pub_date, reverse=True)[:1] #use it later by only selecting more than one trending post
    cats=Category.objects.all()
    recent_posts=posts[:2]
    if trendingposts:
        return {'trending':trendingposts[0],
                'cats':cats,
                'recent_posts':recent_posts,
                }
    else:
        return {'trending':None,
                'cats':cats,
                'recent_posts':recent_posts,
                }