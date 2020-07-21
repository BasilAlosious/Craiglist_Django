import requests
from django.shortcuts import render
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from . import models
# quote_plus = it adds %20 or ++ to a search query and converts it into url

BASE_URL_CRAIGSLIST = 'https://delhi.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request) :

    return render(request, 'base.html')

def new_search(request):
    # Search gets the post request made . ie why post.get. 'search is name of placeholder'

    search = request.POST.get('search')

    models.Search.objects.create(search=search) # to add search obj to db

    final_url = BASE_URL_CRAIGSLIST.format(quote_plus(str(search))) # always convert to string or type error will come

    # requests library is used to make pull requests and fetch websites.

    response = requests.get(final_url)

    data = response.text
    # creates a beautiful soup object and parses it into objects.
    soup = BeautifulSoup(data, features='html.parser')

    # it says find all the a tags with class 'result-title'
    post_listing = soup.find_all('li', {'class': 'result-row'})

    final_postings = []
    post_title = ''
    for post in post_listing :
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        post_time = post.find('time').get('title')

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_time,post_image_url),)

    # dict created to send the search obj to the frontend and display it
    frontend = {'search': search,
                'final_postings': final_postings,
                }

    return render(request, 'my_app/new_search.html', frontend)