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
from .serializers import TweetSerializer
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

@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)
