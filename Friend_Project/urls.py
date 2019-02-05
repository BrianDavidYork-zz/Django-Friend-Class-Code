"""Friend_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Friend_Class.views import UserProfile, AddFriend, DeleteFriend, ShowFriends, ConfirmFriend

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user_profile/(?P<username>[\w.@+-]+)', UserProfile.as_view(), name = 'user_profile'),
    url(r'^add_friend/(?P<username>[\w.@+-]+)', AddFriend.as_view(), name = 'add_friend'),
    url(r'^confirm_friend/(?P<username>[\w.@+-]+)', ConfirmFriend.as_view(), name = 'confirm_friend'),
    url(r'^show_friends/(?P<username>[\w.@+-]+)', ShowFriends.as_view(), name = 'show_friends'),
    url(r'^delete_friend/(?P<username>[\w.@+-]+)', DeleteFriend.as_view(), name = 'delete_friend'),
]
