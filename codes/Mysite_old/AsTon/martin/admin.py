from django.contrib import admin
from martin.models import Movies
#from blog.models import Post
# Register your models here.
class MartinMovies(admin.ModelAdmin):
    #list_display = ['title', 'summary', 'date_new']
    fieldsets = [('av_pics', {'fields': ['pic']}),
                 ('detail_info', {'fields': ['title', 'summary', 'date_new'], 'classes': ['collapse']})
                 ]

#class BlogPost(admin.ModelAdmin):
#   fields = ['title', 'body', 'excerpt', 'created_time', 'author', 'category']

    
admin.site.register(Movies, MartinMovies)    
#admin.site.register(Post, BlogPost)    