from django.contrib import admin
from  .models import Post
# Register your models here.
class BlogPost(admin.ModelAdmin):
    list_display = ['title', 'body']

admin.site.register(Post, BlogPost)    