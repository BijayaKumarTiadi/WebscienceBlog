from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.text import slugify
from django.urls import reverse
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.db.models import Count
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images/')
    add_date = models.DateTimeField(auto_now_add=True, null=True)
    def save(self, *args, **kwargs):
        self.url = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('category_detail', args=[self.url])
    def __str__(self):
        return self.title
    def image_tag(self):
        return format_html(
            '<img src="/media/{}" style="width:40px;height:40px;border-radius:50%;"  />'.format(self.image))



class Tag(models.Model):
    name = models.CharField(max_length=50)
    tag_description=models.CharField(max_length=100)

    @classmethod
    def get_trending_tags(cls, n=5):
        trending_tags = cls.objects.annotate(tag_count=Count('blogpost__tags')).order_by('-tag_count')[:n]
        return trending_tags
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_description = models.CharField(max_length=150,blank=True)
    place=models.CharField(max_length=50,blank=True)
    url = models.SlugField(max_length=100, unique=True,blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    # image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    image = ProcessedImageField(
        upload_to='post_images/',
        # processors=[ResizeToFill(600, 600)],
        format='JPEG',
        options={'quality': 40}
    )
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    reading_time = models.PositiveIntegerField(default=1)
    class Meta:
        ordering=['-pub_date']

    def save(self, *args, **kwargs):
        words_per_minute = 200  # Adjust this value based on your audience
        total_words = len(self.content.split())
        self.reading_time = max(1, round(total_words / words_per_minute))
        if not self.url:#this is to set automaic and manual url for SEO
            self.url = slugify(self.title)
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.category.url, self.url])
    def __str__(self):
        return self.title
    def image_tag(self):
        return format_html(
            '<img src="/media/{}" style="width:40px;height:40px;border-radius:50%;"  />'.format(self.image))


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)#Only for logged in user
    email = models.EmailField(null=True)
    approved_comment = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    comment_text = models.CharField(max_length=350, blank=False)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.comment_user, self.post)