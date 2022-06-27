import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from .utils import is_ajax

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.

def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', context={}, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    query_set = Tweet.objects.all()
    serializer = TweetSerializer(query_set, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    query_set = Tweet.objects.filter(id=tweet_id)
    if not query_set.exists():
        return Response({}, status=404)
    obj = query_set.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    query_set = Tweet.objects.filter(id=tweet_id)
    if not query_set.exists():
        return Response({}, status=404)
    query_set = query_set.filter(user=request.user)
    if not query_set.exist():
        return Response({"message": "You can not delete this Zweet!"}, status=401)
    obj = query_set.first()
    obj.delete()
    return Response({"message": "Your zweet has been deleted!"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        query_set = Tweet.objects.filter(id=tweet_id)
        if not query_set.exists():
            return Response({}, status=404)
        obj = query_set.first()
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'retweet':
            new_zweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
            serializer = TweetSerializer(new_zweet)
            return Response(serializer.data, status=200)
    return Response({}, status=200)

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)
