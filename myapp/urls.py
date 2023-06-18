from django.urls import path
from myapp import views
from .views import *


urlpatterns = [
    path('',views.about,name='about'),
    path('signup',views.signup,name='signup'),
    path('login',views.loginuser,name='loginuser'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('uploadmusic',views.uploadmusic,name='uploadmusic'),
    path('public',views.upload_public,name='upload_public'),
    path('private',views.upload_private,name='upload_private'),
    path('protected',views.upload_protected,name='upload_protected')

]