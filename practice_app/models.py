from django.db import models

class Posts(models.Model):
    timestamp = models.CharField(max_length=100)
    postId = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    postMessage = models.CharField(max_length=500)
    userHex = models.CharField(max_length=500)

class Users(models.Model): 
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    hex = models.CharField(max_length=100)


def __str__(self): 
    return self.title