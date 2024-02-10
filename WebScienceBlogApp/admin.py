from django.contrib import admin
from .models import Category,BlogPost, Comment,Tag
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=('image_tag','title','description','url','add_date')
    search_fields=('title',)

class BlogPostAdmin(admin.ModelAdmin):
    list_display=('image_tag','title','url','pub_date','author','category','views')
    search_fields=('title',)
    list_filter=('category',)
    list_per_page=10
    class Media:
        js = ('https://cdn.tiny.cloud/1/te7j8vbm69gpgqwln72goqvqsxhlf49v6xh1xwmsq6qoowzu/tinymce/5/tinymce.min.js', 'js/tinymceadmin.js',)

class TagAdmin(admin.ModelAdmin):
    list_display=('name','tag_description')
    list_per_page=10
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'parent_comment', 'comment_date','post','approved_comment','reported')
    raw_id_fields = ('parent_comment',)
    list_per_page=10

admin.site.register(Category,CategoryAdmin)
admin.site.register(BlogPost,BlogPostAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)
