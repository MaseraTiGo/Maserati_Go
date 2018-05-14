from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .form import AddForm
# Create your views here.
def index(request):
    return render(request, 'learn/index.html')
    #render(request, 'learn/home.html')

def add(request, a, b):
    return HttpResponse(str(int(a) + int(b)))

def for_loop(request):
    test_list = []#['apple', 'ball', 'canada', 'damn']
    return render(request, 'learn/forloop.html', {'test': test_list})
    
def dict_loop(request):
    test_dict = {'a': 'apple', 'b': 'ball', 'c': 'canada', 'd': 'damn'}
    return render(request, 'learn/dictloop.html', {'test': test_dict})

def add_new(request):
    a = request.GET['a']
    b = request.GET['b']
    c = str(int(a) + int(b))
    return HttpResponse('<h1>fucking result is:%s</h1>'%c)

def index_form(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
    else:
        form = AddForm()
    return render(request, 'learn/index_form.html', {'form': form})