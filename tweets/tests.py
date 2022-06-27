from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Tweet

User = get_user_model()

# Create your tests here.
class ZweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="abc", password='passwwerwer')
        self.user2 = User.objects.create_user(username="xyz", password='passwwe235rwer')
        Tweet.objects.create(content="first zweet", user=self.user)
        Tweet.objects.create(content="2nd zweet", user=self.user)
        Tweet.objects.create(content="3rd zweet", user=self.user2)
        self.currentCount = Tweet.objects.all().count()

    def test_user_created(self):
        self.assertEqual(self.user.username, "abc")

    def test_zweet_created(self):
        tweet_obj = Tweet.objects.create(content="4th zweet", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="passwwerwer")
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
    
    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action", {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_zweet_id = data.get('id')
        self.assertNotEqual(new_zweet_id, 2)
        self.assertEqual(self.currentCount + 1, new_zweet_id)

    def test_zweet_create__api_view(self):
        request_data = {"content": "TEST ZWEET"}
        client = self.get_client()
        response = client.post("/create-tweet", request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_zweet_id = response_data.get('id')
        self.assertEqual(self.currentCount + 1, new_zweet_id)

    def test_zweet_detail_view(self):
        client = self.get_client()
        response = client.get("/tweets/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_zweet_delete_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/tweets/1/delete")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete("/api/tweets/3/delete")
        self.assertEqual(response_incorrect_owner.status_code, 401)
