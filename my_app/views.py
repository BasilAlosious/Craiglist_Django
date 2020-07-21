import requests
from django.shortcuts import render
from bs4 import Beautifulsoup

# Create your views here.
def home(request):
    return render(request,'base.html')


def new_search(request):
    # Search gets the post request made . ie why post.get. 'search is name of placeholder'
    search= request.POST.get('search')

    frontend= {'search':search,
               }
    return render(request,'my_app/new_search.html',frontend)