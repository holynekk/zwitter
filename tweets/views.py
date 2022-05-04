from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet


# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

def tweet_list_view(request, *args, **kwargs):
    query_set = Tweet.objects.all()
    tweet_list = [{'id': x.id, "content": x.content} for x in query_set]
    data = {
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
