from django.shortcuts import render
from martin.models import *
# Create your views here.
def movie_index(request):
    movies = Movies.objects.all()
    return render(request, 'index.html', {'movies': movies})
