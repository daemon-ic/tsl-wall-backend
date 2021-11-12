
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from .serializars import UsersSerializer
from .models import Posts, Users
from email.message import EmailMessage
import smtplib
import uuid
import time


def send_email(toEmail):
    EMAIL_PORT = 465
    EMAIL_SSL = "smtp.gmail.com"
    SENDER_EMAIL = "asewram.spam@gmail.com"
    SENDER_PASSWORD = "Test123!"
    SUBJECT = "Thank you for joining the Wall!"
    CONTENT = "You have successfully created an account with The Wall! Please use the username and password you provided to log in. Enjoy!"
    try: 
        msg = EmailMessage()
        msg["Subject"] = SUBJECT
        msg["From"] = SENDER_EMAIL # NOT SURE WHERE THIS IS USED
        msg["To"] = toEmail
        msg.set_content(CONTENT)
        server = smtplib.SMTP_SSL(EMAIL_SSL, EMAIL_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return "Email Sent!"
    except Exception as e:
        print(e)

class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all() 

class AllPostsView(viewsets.ViewSet):
    def list(self, request, format=None):
        posts = Posts.objects.all()
        dict_posts = []
        for post in posts:
            newPost = model_to_dict(post)
            dict_posts.append(newPost)
        return Response(dict_posts)

class OthersPostsView(viewsets.ViewSet):
     def create(self, request, format=None):
        username = request.data["username"]
        posts = Posts.objects.filter(username=username)
        dict_posts = []
        for post in posts:
            newPost = model_to_dict(post)
            dict_posts.append(newPost)
        return Response(dict_posts)

class ProfileView(viewsets.ViewSet):
    def create(self, request, format=None):
        username = request.data["username"]
        user = Users.objects.get(username=username)
        dict = model_to_dict(user)
        return Response(dict)

class PostsView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, format=None):
      
        username = request.user.username
        postMessage = request.data["postMessage"]
        timestamp = int(round(time.time() * 1000))
        postId = uuid.uuid4()
        user = Users.objects.get(username=username)
        name = user.name
        userHex = user.hex
        newPost = Posts(timestamp=timestamp, username=username, postMessage=postMessage, postId=postId, name=name, userHex=userHex)
        newPost.save()
        return Response("Post Created")

    def list(self, request, format=None):
        username = request.user.username
        posts = Posts.objects.filter(username=username)
        dict_posts = []
        for post in posts:
            newPost = model_to_dict(post)
            dict_posts.append(newPost)
        return Response(dict_posts)


class UserView(viewsets.ViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, format=None):
        username = request.user.username
        user = Users.objects.get(username=username)
        dict = model_to_dict(user)
        return Response(dict)



 
class Register(viewsets.ViewSet):

    def create(self, request, format=None):
        try:
            email = request.data["email"]
            password = request.data["password"]
            name = request.data["name"]
            username = request.data["username"]
            hex = request.data["hex"]
            user = User.objects.create_user(username, email, password)
            user.save()
            newUser = Users(name=name, email=email, username=username, hex=hex)
            newUser.save()
            send_email(email)
            return Response("OK")
        except:
            return Response("NOT OKAY")


class Login(viewsets.ViewSet):
  
    def create(self, request, format=None):
        password = request.data["password"]
        username = request.data["username"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
             return Response("OK")
        else:
              return Response("KO")

class Logout(viewsets.ViewSet):

    def list(self, request, format=None):
        logout(request)


