from django.urls import path, re_path
from .views import home_view, tweet_detail_view, tweet_list_view, tweet_create_view, tweet_delete_view, tweet_action_view

urlpatterns = [
    path('', home_view),
    path('api/tweets/', tweet_list_view),
    path('api/tweets/<int:tweet_id>', tweet_detail_view),
    path('api/create-tweet', tweet_create_view),
    path('api/tweets/action', tweet_action_view),
    path('api/tweets/<int:tweet_id>/delete', tweet_delete_view),
]
