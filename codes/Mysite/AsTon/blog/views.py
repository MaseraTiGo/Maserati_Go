from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
import markdown
# Create your views here.
def blog_index(request):
    #post = get_object_or_404(Post, pk=pk)
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def blog_test(request, pk):
    print('pk_value:', pk)
    post = get_object_or_404(Post, pk=pk)
    print('post_value', post)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',      
                                  ])
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/test.html', context={'post': post})    