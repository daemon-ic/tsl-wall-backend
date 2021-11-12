from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from .models import Posts, Users
from .views import PostsView, UserView
from .views import send_email

client = Client()

def createAuthedUser():
    Users.objects.create(username="alvin", email="asewram.business@gmail.com", name="alvin", hex="#fff")
    user = Users.objects.get(username="alvin")
    user.is_authenticated = True;
    return user;

## CHECKS REGISTRATION
class UserViewTestCase(TestCase):
    def test_get_user(self):
        print("-")
        print("RUNNING CREATE USER TEST")
        request = APIRequestFactory().get("")
        user = createAuthedUser()
        print("Created Test User...")
        force_authenticate(request, user=user)
        print("Force Authenticating User...")
        user_view = UserView.as_view({"get": "list"})
        response = user_view(request)
        print("Checking Response Accuracy...")
        self.assertEqual(response.data["name"], "alvin")

## CHECKS EMAIL CREATION
class EmailTestCase(TestCase):
    def test_create_email(self):
        print("-")
        print("RUNNING EMAIL TEST")
        print("Sending Test Email To asewram.spam@gmail.com By Default...")
        print("Please Change Receiving Email In practice/practice_app/tests.py")
        print("Sending Email...")
        result = send_email("asewram.spam@gmail.com")
        self.assertEqual(result, "Email Sent!")


## CHECKS LOGIN AND POST
class PostsTestCase(TestCase):
    def test_create_post(self):
        print("-")
        print("RUNNING POST TEST")
        request = APIRequestFactory().post("", { "postMessage": "Hello World"})
        user = createAuthedUser()
        print("Created Test User...")
        force_authenticate(request, user=user)
        print("Force Authenticating User...")
        posts_view = PostsView.as_view({'post': 'create'})
        response = posts_view(request)
        post = Posts.objects.get(username=user.username)
        print("Checking Post Accuracy...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.postMessage, "Hello World")

## CHECKS VIEW OF WALL
    def test_get_all_posts(self):
        print("-")
        print("RUNNING WALL TEST")
        request = APIRequestFactory().get("")
        user = createAuthedUser()
        print("Created Test User...")
        force_authenticate(request, user=user)
        print("Force Authenticating User...")
        Posts.objects.create(timestamp=0, username=user.username, postMessage="Test message", postId="123", name=user.name, userHex=user.hex)
        Posts.objects.create(timestamp=0, username=user.username, postMessage="Test message", postId="1234", name=user.name, userHex=user.hex)
        Posts.objects.create(timestamp=0, username=user.username, postMessage="Test message", postId="1235", name=user.name, userHex=user.hex)
        Posts.objects.create(timestamp=0, username=user.username, postMessage="Test message", postId="1236", name=user.name, userHex=user.hex)
        print("Created 4 Test Posts...")
        posts_view = PostsView.as_view({'get': 'list'})
        response = posts_view(request)
        print("Checking Getting All Posts...")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
