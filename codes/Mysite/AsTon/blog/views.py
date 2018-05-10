from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.shortcuts import get_object_or_404
# Create your views here.
def blog_index(request, pk):
    post = get_object_or_404(Post, pk=pk)
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
