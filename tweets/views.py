import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Tweet
from .forms import TweetForm
from .utils import is_ajax

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    query_set = Tweet.objects.all()
    tweet_list = [x.serialize() for x in query_set]
    data = {
        'is_user': False,
        'response': tweet_list,
    }
    return JsonResponse(data)

def tweet_detail_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
        "content": tweet.content,
        # "image_path": tweet.image.url
    }
    status = 200
    try:
        tweet = Tweet.objects.get(id=tweet_id)
        data['content'] = tweet.content
    except:
        data['message'] = 'Not Found'
        status = 404
    
    return JsonResponse(data, status=status)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if is_ajax(request):
            return JsonResponse(obj.serialize(), status=201)
        if next_url and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if is_ajax(request):
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})
