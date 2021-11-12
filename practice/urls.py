"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from practice_app import views
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r"posts", views.PostsView, "post")
router.register(r"others-posts", views.OthersPostsView, "others-post")
router.register(r"all-posts", views.AllPostsView, "post-all")
router.register(r"users", views.UsersView, "user")
router.register(r"user", views.UserView, "user")
router.register(r"profile",views.ProfileView, "profile")
router.register(r"login", views.Login, "auth-login")
router.register(r"logout", views.Logout, "auth-logout")
router.register(r"register", views.Register, "auth-register")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls))
]
